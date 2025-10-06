from langchain_huggingface.embeddings import HuggingFaceEmbeddings

from .device_config import get_device


def create_embeddings(
    model_name: str = "BAAI/bge-large-en-v1.5",
) -> HuggingFaceEmbeddings:
    """Create HuggingFace embeddings with device configuration.

    Args:
        model_name: Name of the embedding model to use

    Returns:
        Configured HuggingFace embeddings instance
    """
    device = get_device()
    return HuggingFaceEmbeddings(model_name=model_name, model_kwargs={"device": device})
