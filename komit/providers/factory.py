from komit.komitconfig import KomitConfig
from komit.providers.base import LLMProvider
from komit.providers.ollama import OllamaProvider
from komit.providers.openai_compatible import OpenAICompatibleProvider


def create_provider(config: KomitConfig) -> LLMProvider:
    if config.provider == "ollama":
        return OllamaProvider(
            model=config.model,
            base_url=config.ollama_url,
            timeout=config.timeout,
        )

    if config.provider == "openai_compatible":
        return OpenAICompatibleProvider(
            model=config.model,
            base_url=config.base_url,
            timeout=config.timeout,
        )

    raise ValueError(f"Unsupported provider: {config.provider}")
