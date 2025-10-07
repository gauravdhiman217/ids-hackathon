import os

from decouple import config
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
from langsmith import traceable

@traceable
def get_model(temperature: float = 0.2) -> BaseChatModel:
    """
    Get a configured chat model with automatic provider fallback.

    Args:
        temperature: Model temperature setting

    Returns:
        Configured chat model instance

    Raises:
        RuntimeError: If no API keys are available
    """

    try:
        # Try Gemini first
        gemini_key: str | None = os.environ.get("GEMINI_API_KEY")
        if gemini_key:
            return init_chat_model(
                model="gemini-2.5-flash",
                model_provider="google_genai",
                api_key=config("GEMINI_API_KEY"),
                temperature=temperature,
            )

        # Fallback to OpenAI
        openai_key: str | None = os.environ.get("OPENAI_API_KEY")
        if openai_key:
            return init_chat_model(
                model="gpt-4.1-nano",
                model_provider="openai",
                temperature=temperature,
            )

        # No valid keys found

        raise RuntimeError(
            "No API keys found. Set GEMINI_API_KEY or OPENAI_API_KEY environment variable."
        )

    except Exception:
        raise
