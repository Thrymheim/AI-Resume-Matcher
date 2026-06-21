from langchain_chroma import Chroma
from .embeddings import get_embeddings
import shutil
import os

CHROMA_DIR = "chroma_db"


def get_vector_store(collection_name: str = "default"):
    embeddings = get_embeddings()
    persist_dir = os.path.join(CHROMA_DIR, collection_name)
    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_dir
    )


def add_documents(texts: list[str], collection_name: str = "default", metadatas: list[dict] = None):
    store = get_vector_store(collection_name)
    store.add_texts(texts=texts, metadatas=metadatas)
    return store


def similarity_search(query: str, collection_name: str = "default", k: int = 5):
    store = get_vector_store(collection_name)
    return store.similarity_search(query, k=k)


def clear_collection(collection_name: str = "default"):
    persist_dir = os.path.join(CHROMA_DIR, collection_name)
    if os.path.exists(persist_dir):
        try:
            shutil.rmtree(persist_dir)
        except PermissionError:
            pass
