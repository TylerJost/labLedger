
from transformers import pipeline
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Summarize text from git commits')
    parser.add_argument('-t','--text', 
                        help='Path to text file to be summarized', 
                        default='/home/tyj566/misc/gitLog.txt')
    parser.add_argument('-d','--datestring', default='')
    args = vars(parser.parse_args())
    
    with open(args['text'], 'r') as f:
        text = f.read()

    date = args['datestring']
    print(f'{date=}')
    toSummarize = []
    summarize = 0
    for line in text.splitlines():
        if line.startswith(date):
            summarize = 1
            print('Set summarizing')
        if line.startswith("repository: "):
            continue
        elif line == "":
            continue
        elif summarize:
            lineParts = line.split(" ")
            lineText = " ".join(lineParts[2:])
            toSummarize.append(lineText)
    print(toSummarize)
    if len(toSummarize) == 0:
        exit('Nothing to summarize, exiting')

    text = ". ".join(toSummarize)
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=500, min_length=30, do_sample=False)[0]['summary_text']
    with open(args['text'], 'a') as f:
        f.write(f"\nSummary:\n{summary}\n")
