"""Device configuration for GPU/CPU selection."""

import torch


def get_device() -> str:
    """Get the appropriate device for model inference.

    Returns:
        Device string: 'cuda' if available, otherwise 'cpu'
    """
    return "cuda" if torch.cuda.is_available() else "cpu"
