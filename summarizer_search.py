# %%
import datetime
import os
from pathlib import Path

from langchain_anthropic import ChatAnthropic
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# %%
filterDate = (datetime.datetime.now() - datetime.timedelta(days=7)).timestamp()
# 0. Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
)

retriever = vector_db.as_retriever(
    search_kwargs={
        "k": 20, # Increase k to ensure we don't 'cap' the results too early
        "filter": {
            "repo": "clusterCleaver-analysis" 
        }
    }
)

# 1. LLM
llm = ChatAnthropic(
    model="claude-sonnet-4-5-20250929",
    temperature=0,
)

# 2. Prompt
prompt = ChatPromptTemplate.from_template("""
You are a Senior Technical Lead and Scientist. Your goal is to review the following git commits 
and provide a concise, high-signal standup report for the team.

CONTEXT (Commits from the database):
{context}

USER REQUEST:
{input}

Please provide your response in the following Markdown format:

### Standup Summary
*Summarize the main technical achievements and progress made.*

### Commit Quality Audit
*For each commit provided in the context, give a score (0-10) and a 1-sentence critique.*
- **[Hash]**: [Score]/10 - [Critique]

### Senior Advice
*Provide one specific piece of advice to improve the commit history or coding workflow based on these changes.*
""")

# 3. Format retrieved docs into a single string
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# 4. Build LCEL retrieval chain (modern way)
rag_chain = (
    {
        "context": retriever | format_docs,
        "input": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)
# %%
# 5. Run
query = "What have we done with regards to RNA sequencing"

response = rag_chain.invoke(query)

print(response)
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