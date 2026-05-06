import pytest
from unittest.mock import MagicMock, patch
from komit.komitconfig import KomitConfig
from komit.generator import generate_message, STYLES


class TestStyles:
    def test_all_three_styles_exist(self):
        assert "conventional" in STYLES
        assert "simple" in STYLES
        assert "detailed" in STYLES

    def test_each_style_is_non_empty_string(self):
        for name, prompt in STYLES.items():
            assert isinstance(prompt, str), f"Style '{name}' is not a string"
            assert len(prompt) > 0, f"Style '{name}' is empty"

    def test_conventional_mentions_types(self):
        assert "feat" in STYLES["conventional"]
        assert "fix" in STYLES["conventional"]

    def test_simple_mentions_imperative(self):
        assert "imperative" in STYLES["simple"].lower()

    def test_detailed_mentions_bullet(self):
        assert "-" in STYLES["detailed"]


class TestDiffTruncation:
    def _make_mock_response(self, content="feat: test"):
        mock_response = MagicMock()
        mock_response.message.content = content
        return mock_response

    # Client is imported lazily inside generate_message(), so we patch at the
    # source: ollama.Client — not komit.generator.Client.
    @patch("ollama.Client")
    def test_short_diff_is_not_truncated(self, mock_client_cls):
        mock_client_cls.return_value.chat.return_value = self._make_mock_response()
        config = KomitConfig(max_diff_length=4000)
        diff = "small diff"
        generate_message(diff, config)
        call_args = mock_client_cls.return_value.chat.call_args
        user_content = call_args.kwargs["messages"][1]["content"]
        assert "truncated" not in user_content

    @patch("ollama.Client")
    def test_long_diff_is_truncated(self, mock_client_cls):
        mock_client_cls.return_value.chat.return_value = self._make_mock_response()
        config = KomitConfig(max_diff_length=100)
        diff = "x" * 200
        generate_message(diff, config)
        call_args = mock_client_cls.return_value.chat.call_args
        user_content = call_args.kwargs["messages"][1]["content"]
        assert "truncated" in user_content

    @patch("ollama.Client")
    def test_truncated_diff_respects_max_length(self, mock_client_cls):
        mock_client_cls.return_value.chat.return_value = self._make_mock_response()
        config = KomitConfig(max_diff_length=50)
        diff = "a" * 200
        generate_message(diff, config)
        call_args = mock_client_cls.return_value.chat.call_args
        user_content = call_args.kwargs["messages"][1]["content"]
        assert len(user_content) < 200 + 100


class TestStylePromptSelection:
    def _make_mock_response(self, content="feat: test"):
        mock_response = MagicMock()
        mock_response.message.content = content
        return mock_response

    @patch("ollama.Client")
    def test_conventional_style_sends_correct_prompt(self, mock_client_cls):
        mock_client_cls.return_value.chat.return_value = self._make_mock_response()
        config = KomitConfig(style="conventional")
        generate_message("diff", config)
        system_content = mock_client_cls.return_value.chat.call_args.kwargs["messages"][0]["content"]
        assert system_content == STYLES["conventional"]

    @patch("ollama.Client")
    def test_simple_style_sends_correct_prompt(self, mock_client_cls):
        mock_client_cls.return_value.chat.return_value = self._make_mock_response()
        config = KomitConfig(style="simple")
        generate_message("diff", config)
        system_content = mock_client_cls.return_value.chat.call_args.kwargs["messages"][0]["content"]
        assert system_content == STYLES["simple"]

    @patch("ollama.Client")
    def test_detailed_style_sends_correct_prompt(self, mock_client_cls):
        mock_client_cls.return_value.chat.return_value = self._make_mock_response()
        config = KomitConfig(style="detailed")
        generate_message("diff", config)
        system_content = mock_client_cls.return_value.chat.call_args.kwargs["messages"][0]["content"]
        assert system_content == STYLES["detailed"]

    @patch("ollama.Client")
    def test_unknown_style_falls_back_to_conventional_prompt(self, mock_client_cls):
        """Fix #10: fallback must be the actual prompt, not the string 'conventional'."""
        mock_client_cls.return_value.chat.return_value = self._make_mock_response()
        config = KomitConfig(style="nonexistent_style")
        generate_message("diff", config)
        system_content = mock_client_cls.return_value.chat.call_args.kwargs["messages"][0]["content"]
        assert system_content == STYLES["conventional"]
        assert system_content != "conventional"


class TestGenerateMessageReturn:
    def _make_mock_response(self, content):
        mock_response = MagicMock()
        mock_response.message.content = content
        return mock_response

    @patch("ollama.Client")
    def test_returns_stripped_string(self, mock_client_cls):
        mock_client_cls.return_value.chat.return_value = self._make_mock_response("  feat: add thing  ")
        result = generate_message("diff")
        assert result == "feat: add thing"

    @patch("ollama.Client")
    def test_returns_correct_message(self, mock_client_cls):
        mock_client_cls.return_value.chat.return_value = self._make_mock_response("fix: resolve null pointer")
        result = generate_message("diff", KomitConfig())
        assert result == "fix: resolve null pointer"

    @patch("ollama.Client")
    def test_uses_default_config_when_none_passed(self, mock_client_cls):
        mock_client_cls.return_value.chat.return_value = self._make_mock_response("chore: update deps")
        result = generate_message("diff", None)
        assert result == "chore: update deps"
        call_kwargs = mock_client_cls.return_value.chat.call_args.kwargs
        assert call_kwargs["model"] == "qwen2.5:7b"


class TestGenerateMessageErrors:
    @patch("ollama.Client")
    def test_ollama_exception_raises_runtime_error(self, mock_client_cls):
        mock_client_cls.return_value.chat.side_effect = Exception("connection refused")
        with pytest.raises(RuntimeError, match="Failed to generate commit message"):
            generate_message("diff", KomitConfig())

    @patch("ollama.Client")
    def test_runtime_error_contains_original_message(self, mock_client_cls):
        mock_client_cls.return_value.chat.side_effect = Exception("model not found")
        with pytest.raises(RuntimeError, match="model not found"):
            generate_message("diff", KomitConfig())

    @patch("komit.generator.model_exist", return_value=True)
    @patch("komit.generator.check_ollama_running", return_value=True)
    @patch("ollama.Client")
    def test_client_receives_correct_ollama_url(
            self,
            mock_client_cls,
            mock_check,
            mock_model_exist
    ):
        mock_client_instance = MagicMock()
        mock_client_instance.chat.return_value.message.content = "feat: x"
        mock_client_cls.return_value = mock_client_instance

        config = KomitConfig(ollama_url="http://myhost:11434")

        generate_message("diff", config)

        mock_client_cls.assert_called_once_with(host="http://myhost:11434")