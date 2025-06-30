import pandas as pd
from langchain_community.vectorstores import Chroma
#from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import tempfile
import os
from dotenv import load_dotenv
load_dotenv()

embedding_model = OpenAIEmbeddings()


def store_rag_to_chroma(rag_text: str, product_title: str):
    """
    Store uploaded RAG text into ChromaDB under a specific namespace (product_title).
    Each paragraph/chunk becomes a searchable document.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    chunks = splitter.split_text(rag_text)
    docs = [Document(page_content=chunk) for chunk in chunks if chunk.strip()]

    persist_dir = os.path.join("chroma_store", product_title)
    db = Chroma.from_documents(docs, embedding_model, persist_directory=persist_dir)
    db.persist()

def load_rag_knowledge(product_title: str, query: str, k: int = 5) -> str:
    """
    Perform a similarity search on the stored RAG documents using the query.
    Returns concatenated top-k documents as additional context.
    """
    persist_dir = os.path.join("chroma_store", product_title)
    db = Chroma(persist_directory=persist_dir, embedding_function=embedding_model)
    matches = db.similarity_search(query, k=k)
    return "\n---\n".join([m.page_content for m in matches])

def store_excel_to_chroma(file, namespace):
    df = pd.read_excel(file)
    text_chunks = []

    for _, row in df.iterrows():
        line = f"Dev: {row.get('Developer')}\nTask: {row.get('Task Description')}\nDomain: {row.get('Domain', '')}"
        text_chunks.append(Document(page_content=line))

    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    docs = splitter.split_documents(text_chunks)

    persist_dir = os.path.join("chroma_store", namespace)
    db = Chroma.from_documents(docs, embedding_model, persist_directory=persist_dir)
    db.persist()


def get_similar_team_profiles(query: str, dev_name: str, product_title: str, k: int = 3):
    persist_dir = os.path.join("chroma_store", product_title)
    db = Chroma(persist_directory=persist_dir, embedding_function=embedding_model)
    results = db.similarity_search(query, k=k)
    return [r.page_content for r in results if dev_name in r.page_content]


'''def store_rag_to_chroma(rag_text: str, product_title: str):
    """
    Store uploaded RAG text into ChromaDB under a specific namespace (product_title).
    Each paragraph/chunk becomes a searchable document.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    chunks = splitter.split_text(rag_text)
    docs = [Document(page_content=chunk) for chunk in chunks if chunk.strip()]

    persist_dir = os.path.join("chroma_store", product_title)
    db = Chroma.from_documents(docs, embedding_model, persist_directory=persist_dir)
    db.persist()'''