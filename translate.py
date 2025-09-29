from transformers import pipeline
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Summarize text from git commits')
    parser.add_argument('-t','--text', 
                        help='Path to text file to be summarized', 
                        default='/home/tyj566/misc/gitLog.txt')
    args = vars(parser.parse_args())
    
    with open(args['text'], 'r') as f:
        text = f.read()

    toSummarize = []
    for line in text.splitlines():
        if line.startswith("==="):
            continue
        elif line == "":
            continue
        else:
            lineParts = line.split(" ")
            lineText = " ".join(lineParts[2:])
            toSummarize.append(lineText)
    text = ". ".join(toSummarize)
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=500, min_length=30, do_sample=False)[0]['summary_text']
    with open(args['text'], 'a') as f:
        f.write(f"\n=== SUMMARY ===\n{summary}\n")
