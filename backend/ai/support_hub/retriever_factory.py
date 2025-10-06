"""Retriever factory for different search strategies."""

from typing import Any, Dict

from langchain.chat_models import init_chat_model
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.retrievers import BaseRetriever
from langchain_core.vectorstores import VectorStore


def create_similarity_retriever(vector_store: VectorStore, k: int = 5) -> BaseRetriever:
    """Create similarity search retriever.

    Args:
        vector_store: Vector store instance
        k: Number of documents to retrieve

    Returns:
        Configured similarity retriever
    """
    return vector_store.as_retriever(search_type="similarity", search_kwargs={"k": k})


def create_mmr_retriever(
    vector_store: VectorStore, k: int = 5, lambda_mult: float = 0.5
) -> BaseRetriever:
    """Create MMR (Maximum Marginal Relevance) retriever.

    Args:
        vector_store: Vector store instance
        k: Number of documents to retrieve
        lambda_mult: Diversity parameter (0=max diversity, 1=min diversity)

    Returns:
        Configured MMR retriever
    """
    return vector_store.as_retriever(
        search_type="mmr", search_kwargs={"k": k, "lambda_mult": lambda_mult}
    )


def create_multi_query_retriever(
    vector_store: VectorStore,
    model_name: str = "gemini-2.5-flash",
    model_provider: str = "google_genai",
    k: int = 4,
    lambda_mult: float = 0.5,
) -> MultiQueryRetriever:
    """Create multi-query retriever with LLM.

    Args:
        vector_store: Vector store instance
        model_name: LLM model name
        model_provider: LLM provider
        k: Number of documents to retrieve
        lambda_mult: MMR diversity parameter

    Returns:
        Configured multi-query retriever
    """
    llm = init_chat_model(model_name, model_provider=model_provider)
    base_retriever = create_mmr_retriever(vector_store, k, lambda_mult)

    return MultiQueryRetriever.from_llm(retriever=base_retriever, llm=llm)
