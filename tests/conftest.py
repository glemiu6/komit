# tests/conftest.py
import sys
from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def mock_git_context():
    with (
        patch("komit.generator.get_changed_files", return_value=[]),
        patch("komit.generator.get_recent_commits", return_value=""),
        patch("komit.main.check_for_updates"),
    ):
        yield


@pytest.fixture(autouse=True)
def reset_argv():
    with patch.object(sys, "argv", ["komit"]):
        yield
