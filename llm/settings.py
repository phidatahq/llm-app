from pydantic import BaseSettings


class LLMSettings(BaseSettings):
    """LLM settings that can be derived from environment variables.

    Reference: https://pydantic-docs.helpmanual.io/usage/settings/
    """

    chat_model: str = "gpt-4"
    condense_model: str = "gpt-3.5-turbo"
    embedding_model: str = "ada"
    default_max_tokens: int = 1024
    default_temperature: float = 0.0


# Create LLMSettings object
llm_settings = LLMSettings()
