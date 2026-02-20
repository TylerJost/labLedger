# %%
from pathlib import Path

from langchain_community.document_loaders import GitLoader
# %%
repoPath = Path('/home/tyler/Documents/hePred')

loader = GitLoader(repo_path=repoPath, branch="main")
# %%
documents = loader.load()
# %%
# 4. Quick check: Let's see the most recent commit
print(f"Total commits indexed: {len(documents)}")
if documents:
    print(f"Sample Message: {documents[0].page_content}")
    print(f"Sample Metadata: {documents[0].metadata}")
