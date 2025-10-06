"""Main support hub search functionality."""

from .embedding_factory import create_embeddings
from .retriever_factory import (create_mmr_retriever,
                                create_multi_query_retriever,
                                create_similarity_retriever)
from .vector_store_factory import create_vector_store


class SupportHubSearch:
    """Main class for support hub search functionality."""

    def __init__(self, index_name: str = "faqs"):
        """Initialize support hub search.

        Args:
            index_name: Pinecone index name
        """
        self.embeddings = create_embeddings()
        self.vector_store = create_vector_store(index_name, self.embeddings)

    def similarity_search(self, query: str, k: int = 3):
        """Perform similarity search.

        Args:
            query: Search query
            k: Number of results

        Returns:
            Search results
        """
        return self.vector_store.similarity_search(query, k=k)

    def get_similarity_retriever(self, k: int = 5):
        """Get similarity retriever."""
        return create_similarity_retriever(self.vector_store, k)

    def get_mmr_retriever(self, k: int = 5, lambda_mult: float = 0.5):
        """Get MMR retriever."""
        return create_mmr_retriever(self.vector_store, k, lambda_mult)

    def get_multi_query_retriever(self, k: int = 4, lambda_mult: float = 0.5):
        """Get multi-query retriever."""
        return create_multi_query_retriever(
            self.vector_store, k=k, lambda_mult=lambda_mult
        )
