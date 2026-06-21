from langchain_huggingface import HuggingFaceEmbeddings
from django.conf import settings
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

_embedding_instance = None


def get_embeddings():
    global _embedding_instance
    if _embedding_instance is None:
        _embedding_instance = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"}
        )
    return _embedding_instance
