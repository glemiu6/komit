"""Unit tests for the provider-independent commit generator."""

from unittest.mock import Mock, patch

import httpx
import pytest

from komit.generator import STYLES, explain_changes, generate_message, summarize_file_chunk
from komit.komitconfig import KomitConfig


@pytest.fixture
def mock_provider():
    """Mock the generator's provider boundary, not an individual LLM SDK."""
    provider = Mock()
    provider.generate.return_value = "feat: add support"
    with patch("komit.generator._create_checked_provider", return_value=provider) as factory:
        yield provider, factory


def _system_prompt(provider):
    return provider.generate.call_args.kwargs["system_prompt"]


def _user_prompt(provider):
    return provider.generate.call_args.kwargs["user_prompt"]


class TestStyles:
    def test_all_three_styles_exist(self):
        assert {"conventional", "simple", "detailed"} <= STYLES.keys()

    @pytest.mark.parametrize("style", ["conventional", "simple", "detailed"])
    def test_styles_are_nonempty(self, style):
        assert isinstance(STYLES[style], str)
        assert STYLES[style]

    def test_conventional_prompt_mentions_types(self):
        assert "feat" in STYLES["conventional"]
        assert "fix" in STYLES["conventional"]

    def test_simple_prompt_requires_imperative(self):
        assert "imperative" in STYLES["simple"].lower()

    def test_detailed_prompt_mentions_bullet_points(self):
        assert "bullet" in STYLES["detailed"].lower()


class TestDiffHandling:
    def test_small_diff_is_in_prompt(self, mock_provider):
        provider, _ = mock_provider
        generate_message("small diff", KomitConfig(max_diff_length=100))
        assert "small diff" in _user_prompt(provider)
        assert "truncated" not in _user_prompt(provider)

    def test_large_diff_is_truncated(self, mock_provider):
        provider, _ = mock_provider
        diff = "x" * 300
        message, truncated = generate_message(diff, KomitConfig(max_diff_length=80))
        assert message == "feat: add support"
        assert "truncated" in _user_prompt(provider)
        assert truncated

    def test_large_diff_obeys_context_limit(self, mock_provider):
        provider, _ = mock_provider
        generate_message("x" * 500, KomitConfig(max_diff_length=75))
        sent_diff = _user_prompt(provider).split("Git Diff:\n", 1)[1]
        assert sent_diff.startswith("diff --git ")
        assert sent_diff.endswith("\n... (truncated)")
        assert len(sent_diff.split("\n... (truncated)", 1)[0]) == 75

    def test_deep_mode_summarizes_then_generates(self, mock_provider):
        provider, factory = mock_provider
        provider.generate.side_effect = ["change authentication", "feat: improve login"]
        diff = "diff --git a/auth.py b/auth.py\n@@ -1 +1 @@\n-old\n+new\n"
        message, truncated = generate_message(diff, deep=True)
        assert message == "feat: improve login"
        assert truncated is None
        assert provider.generate.call_count == 2
        assert "File summaries:" in provider.generate.call_args.kwargs["user_prompt"]
        factory.assert_called_once()


class TestPromptSelection:
    @pytest.mark.parametrize("style", ["conventional", "simple", "detailed"])
    def test_prompt_includes_selected_style(self, mock_provider, style):
        provider, _ = mock_provider
        generate_message("diff", KomitConfig(style=style))
        assert STYLES[style] in _system_prompt(provider)

    def test_unknown_style_falls_back_to_conventional(self, mock_provider):
        provider, _ = mock_provider
        generate_message("diff", KomitConfig(style="unknown"))
        assert STYLES["conventional"] in _system_prompt(provider)

    def test_branch_name_is_passed_to_system_prompt(self, mock_provider):
        provider, _ = mock_provider
        generate_message("diff", branch_info="feat/auth-login")
        prompt = _system_prompt(provider)
        assert "feat/auth-login" in prompt
        assert "INFERRED COMMIT TYPE: feat" in prompt

    def test_absent_branch_is_not_invented(self, mock_provider):
        provider, _ = mock_provider
        generate_message("diff")
        assert "No branch name is available" in _system_prompt(provider)


class TestGenerateMessage:
    def test_returns_stripped_string(self, mock_provider):
        provider, _ = mock_provider
        provider.generate.return_value = "  feat: add feature  "
        message, _ = generate_message("diff")
        assert message == "feat: add feature"

    def test_returns_message_and_truncation_list(self, mock_provider):
        message, truncated = generate_message("diff")
        assert message == "feat: add support"
        assert truncated == []

    def test_default_config_is_passed_to_factory(self, mock_provider):
        _, factory = mock_provider
        generate_message("diff", None)
        config = factory.call_args.args[0]
        assert isinstance(config, KomitConfig)
        assert config.model == "qwen2.5:7b"

    def test_custom_model_is_passed_to_factory(self, mock_provider):
        _, factory = mock_provider
        generate_message("diff", KomitConfig(model="mistral:7b"))
        assert factory.call_args.args[0].model == "mistral:7b"

    def test_provider_error_is_wrapped(self, mock_provider):
        provider, _ = mock_provider
        provider.generate.side_effect = ValueError("connection refused")
        with pytest.raises(RuntimeError, match="connection refused"):
            generate_message("diff")

    def test_provider_timeout_has_clear_message(self, mock_provider):
        provider, _ = mock_provider
        provider.generate.side_effect = httpx.TimeoutException("timeout")
        with pytest.raises(RuntimeError, match="Generation timed out"):
            generate_message("diff", KomitConfig(timeout=5))

    def test_malformed_output_is_rejected(self, mock_provider):
        provider, _ = mock_provider
        provider.generate.return_value = "Here is your message: feat: add support"
        with pytest.raises(RuntimeError, match="Conventional Commit"):
            generate_message("diff")

    def test_non_string_output_is_rejected(self, mock_provider):
        provider, _ = mock_provider
        provider.generate.return_value = None
        with pytest.raises(RuntimeError, match="non-text"):
            generate_message("diff")


class TestSummarization:
    def test_returns_filename_prefixed_summary(self, mock_provider):
        provider, _ = mock_provider
        provider.generate.return_value = "updated authentication"
        assert summarize_file_chunk("auth.py", "diff") == ("auth.py: updated authentication")

    def test_uses_correct_model_configuration(self, mock_provider):
        _, factory = mock_provider
        summarize_file_chunk("auth.py", "diff", KomitConfig(model="mistral:7b"))
        assert factory.call_args.args[0].model == "mistral:7b"

    def test_summary_raises_on_provider_error(self, mock_provider):
        provider, _ = mock_provider
        provider.generate.side_effect = ValueError("server offline")
        with pytest.raises(RuntimeError, match="server offline"):
            summarize_file_chunk("auth.py", "diff")

    def test_empty_summary_is_rejected(self, mock_provider):
        provider, _ = mock_provider
        provider.generate.return_value = "  "
        with pytest.raises(RuntimeError, match="empty summary"):
            summarize_file_chunk("auth.py", "diff")

    def test_explain_changes_uses_provider(self, mock_provider):
        provider, _ = mock_provider
        provider.generate.return_value = "Updated the authentication flow"
        explanation = explain_changes("diff")
        assert explanation == "Updated the authentication flow"
        assert "Explain these changes" in _user_prompt(provider)

    def test_explanation_is_truncated(self, mock_provider):
        provider, _ = mock_provider
        explain_changes("a" * 100, KomitConfig(max_diff_length=20))
        assert "truncated" in _user_prompt(provider)
