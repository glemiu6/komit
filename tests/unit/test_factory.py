"""Verify provider selection separately from commit generation."""

from unittest.mock import patch

import pytest

from komit.komitconfig import KomitConfig
from komit.providers.factory import create_provider


def test_creates_ollama_with_correct_url():
    config = KomitConfig(provider="ollama", model="mistral:7b", ollama_url="http://host:11434")
    with patch("komit.providers.factory.OllamaProvider") as provider_class:
        assert create_provider(config) is provider_class.return_value
        provider_class.assert_called_once_with(
            model="mistral:7b", base_url="http://host:11434", timeout=60
        )


def test_creates_openai_compatible_provider():
    config = KomitConfig(provider="openai_compatible", model="qwen", base_url="http://host:8080/v1")
    with patch("komit.providers.factory.OpenAICompatibleProvider") as provider_class:
        assert create_provider(config) is provider_class.return_value
        provider_class.assert_called_once_with(
            model="qwen", base_url="http://host:8080/v1", timeout=60
        )


def test_rejects_unknown_provider():
    with pytest.raises(ValueError, match="Unsupported provider"):
        create_provider(KomitConfig(provider="missing"))
