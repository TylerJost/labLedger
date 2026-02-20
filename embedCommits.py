# %%
from pathlib import Path
from datetime import datetime, timedelta
from git import Repo
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
# %%
repo_path = Path("/home/tyler/Documents/hePred")
db_path = "./chroma_db"

repo = Repo(repo_path)
seven_days_ago = datetime.now() - timedelta(days=7)
commits = list(repo.iter_commits('main', since=seven_days_ago))
# %%
docs = []
for commit in commits:
    # We combine the message and the files changed for the LLM to 'read'
    content = f"Commit: {commit.message}\nFiles changed: {list(commit.stats.files.keys())}"
    
    # We store the metadata so we can filter by date or author later
    metadata = {
        "hash": commit.hexsha,
        "date": str(commit.authored_datetime),
        "author": commit.author.name
    }
    docs.append(Document(page_content=content, metadata=metadata))
# %%
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# %%
vector_db = Chroma.from_documents(
    documents=docs, 
    embedding=embeddings, 
    persist_directory=db_path
)
# %%
vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
print(f"Total records: {vector_db._collection.count()}")

# 2. "Peek" at the first 5 records (Raw look)
# This returns IDs, Documents, and Metadatas
raw_data = vector_db._collection.peek(5)
print(raw_data['documents'])
# %%
query = "That time I looked for an image the was the same"
results = vector_db.similarity_search(query, k=3)

for doc in results:
    print(f"--- Result (Date: {doc.metadata['date']}) ---")
    print(doc.page_content)