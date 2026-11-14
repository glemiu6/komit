"""Deterministic syntax checks for model-generated commit messages."""

import re

_CONVENTIONAL_TITLE = re.compile(
    r"^(?:feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert)"
    r"(?:\([A-Za-z0-9][A-Za-z0-9._/-]*\))?!?: \S.*$"
)


def validate_commit_message(message: str, style: str = "conventional") -> None:
    """Raise ValueError when a generated message has invalid syntax.

    Syntax checks cannot establish whether the description accurately reflects the diff.
    """
    if not message or not message.strip():
        raise ValueError("The model returned an empty commit message.")
    if "\x00" in message:
        raise ValueError("Commit messages must not contain NUL characters.")

    lines = message.splitlines()
    if any(line.strip().startswith("```") for line in lines):
        raise ValueError("The model returned a Markdown code block.")
    if style != "detailed" and len(lines) != 1:
        raise ValueError("This commit style requires a single-line message.")
    if not lines[0].strip():
        raise ValueError("Commit message subject cannot be empty.")
    if style == "conventional" and not _CONVENTIONAL_TITLE.fullmatch(lines[0]):
        raise ValueError(
            "Expected a Conventional Commit subject such as "
            "'feat: add configuration validation'."
        )
