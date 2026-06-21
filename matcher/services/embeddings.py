from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)

_embedding_instance = None


def get_embeddings():
    global _embedding_instance
    if _embedding_instance is not None:
        return _embedding_instance

    try:
        from langchain_huggingface import HuggingFaceEmbeddings
        _embedding_instance = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"}
        )
        logger.info("Using local embeddings")
        return _embedding_instance
    except Exception as e:
        logger.warning(f"Local embeddings failed: {e}, falling back to API")

    from .embeddings_api import APIEmbeddings
    _embedding_instance = APIEmbeddings()
    logger.info("Using API embeddings")
    return _embedding_instance
