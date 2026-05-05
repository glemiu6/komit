import pytest
from komit.komitconfig import KomitConfig


class TestKomitConfigDefaults:
    def test_default_model(self):
        config = KomitConfig()
        assert config.model == "qwen2.5:7b"

    def test_default_style(self):
        config = KomitConfig()
        assert config.style == "conventional"

    def test_default_max_diff_length(self):
        config = KomitConfig()
        assert config.max_diff_length == 4000

    def test_default_ollama_url(self):
        config = KomitConfig()
        assert config.ollama_url == "http://localhost:11434"


class TestKomitConfigCustom:
    def test_custom_model(self):
        config = KomitConfig(model="llama3.2:3b")
        assert config.model == "llama3.2:3b"

    def test_custom_style(self):
        config = KomitConfig(style="simple")
        assert config.style == "simple"

    def test_custom_max_diff_length(self):
        config = KomitConfig(max_diff_length=1000)
        assert config.max_diff_length == 1000

    def test_custom_ollama_url(self):
        config = KomitConfig(ollama_url="http://192.168.1.10:11434")
        assert config.ollama_url == "http://192.168.1.10:11434"

    def test_all_custom(self):
        config = KomitConfig(
            model="mistral:7b",
            style="detailed",
            max_diff_length=2000,
            ollama_url="http://remotehost:11434",
        )
        assert config.model == "mistral:7b"
        assert config.style == "detailed"
        assert config.max_diff_length == 2000
        assert config.ollama_url == "http://remotehost:11434"


class TestKomitConfigEquality:
    def test_two_defaults_are_equal(self):
        assert KomitConfig() == KomitConfig()

    def test_different_configs_are_not_equal(self):
        assert KomitConfig(model="llama3.2:3b") != KomitConfig(model="mistral:7b")