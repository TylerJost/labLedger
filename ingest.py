# %%
from pathlib import Path
from datetime import datetime, timedelta
from git import Repo
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from tqdm import tqdm
# %%
# Inputs
repoPaths = [Path("/home/tyler/Documents/hePred"), Path("/home/tyler/Documents/clusterCleaver-analysis")]
db_path = "./chroma_db"

# Initialize/activate vector database
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings)
# %%
def generateDocs(repo, vector_db, days=7):
    docs = []
    past_time = datetime.now() - timedelta(days=days)
    commits = list(repo.iter_commits('main', since=past_time))
    existing_ids = vector_db.get()['metadatas']
    seen_hashes = {m['hash'] for m in existing_ids}
    docs = []
    for commit in tqdm(commits):
        if commit.hexsha in seen_hashes:
            continue
        content = f"Commit: {commit.message}\nFiles changed: {list(commit.stats.files.keys())}"
        
        # We store the metadata so we can filter by date or author later
        metadata = {
            "hash": commit.hexsha,
            "timestamp": commit.authored_datetime.timestamp(),
            "date_string": str(commit.authored_datetime),
            "author": commit.author.name,
            "repo": Path(repo.working_dir).name
        }
        docs.append(Document(page_content=content, metadata=metadata))
    
    return docs

allDocs = []
for repoPath in repoPaths:
    repo = Repo(repoPath)
    allDocs += generateDocs(repo, vector_db, days=365*5)

# Update database
if len(allDocs)>0:
    vector_db.add_documents(
        documents=allDocs, 
        embedding=embeddings, 
        persist_directory=db_path
    )
# %%
import pandas as pd

# Fetch everything from the collection
data = vector_db.get(include=["metadatas", "documents"])

# Convert to a list of dicts for Pandas
rows = []
for i in range(len(data['ids'])):
    row = data['metadatas'][i]
    row['content_snippet'] = data['documents'][i][:50] + "..."
    rows.append(row)

df = pd.DataFrame(rows)
# %%
results = vector_db.similarity_search(
    "RNA",
    k=5,
    filter={"repo": "clusterCleaver-analysis"}

)
for res in results:
    # print(f"* {res.page_content} [{res.metadata}]")
    print(f"{res.page_content.split('\n')[0]}")