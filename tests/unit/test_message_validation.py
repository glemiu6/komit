import pytest

from komit.message_validation import validate_commit_message


@pytest.mark.parametrize(
    "message",
    [
        "feat: add configuration",
        "fix(cli): handle Git errors",
        "docs!: update public API [feature/docs]",
        "refactor(core): simplify generation",
    ],
)
def test_accepts_valid_conventional_messages(message):
    validate_commit_message(message)


@pytest.mark.parametrize(
    "message",
    [
        "",
        "Here is the commit message:",
        "Add support for model selection",
        "feat: update\nfix: update another feature",
        "```\nfeat: update\n```",
        "unknown: change feature",
    ],
)
def test_rejects_invalid_conventional_messages(message):
    with pytest.raises(ValueError):
        validate_commit_message(message)


def test_simple_style_accepts_plain_title():
    validate_commit_message("Add model selection", "simple")


def test_simple_style_rejects_multiple_lines():
    with pytest.raises(ValueError):
        validate_commit_message("Add model selection\nAnother line", "simple")


def test_detailed_style_accepts_body():
    validate_commit_message("feat: add support\n\n- Add configuration\n- Update docs", "detailed")


def test_rejects_nul_characters():
    with pytest.raises(ValueError):
        validate_commit_message("feat: invalid\x00message")
