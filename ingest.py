# %%
from pathlib import Path
from datetime import datetime, timedelta
from git import Repo
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
# %%
# Inputs
repoPaths = [Path("/home/tyler/Documents/hePred")]
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
    for commit in commits:
        if commit.hexsha in seen_hashes:
            continue
        content = f"Commit: {commit.message}\nFiles changed: {list(commit.stats.files.keys())}"
        
        # We store the metadata so we can filter by date or author later
        metadata = {
            "hash": commit.hexsha,
            "date": str(commit.authored_datetime),
            "author": commit.author.name
        }
        docs.append(Document(page_content=content, metadata=metadata))
    
    return docs

allDocs = []
for repoPath in repoPaths:
    repo = Repo(repoPath)
    allDocs += generateDocs(repo, vector_db, days=100)

# Update database
vector_db.add_documents(
    documents=allDocs, 
    embedding=embeddings, 
    persist_directory=db_path
)
# %%