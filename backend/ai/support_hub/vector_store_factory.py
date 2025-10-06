from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone


def create_vector_store(
    index_name: str, embeddings: HuggingFaceEmbeddings = None
) -> PineconeVectorStore:
    """Create Pinecone vector store with embeddings.

    Args:
        index_name: Name of the Pinecone index
        embeddings: HuggingFace embeddings instance

    Returns:
        Configured Pinecone vector store

    Raises:
        ValueError: If embeddings is None
    """
    if embeddings is None:
        raise ValueError("Embeddings instance is required")

    pc = Pinecone()
    index = pc.Index(name=index_name)

    return PineconeVectorStore(index=index, embedding=embeddings)
