# tests/conftest.py
import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_git_context():
    with patch("komit.generator.get_changed_files", return_value=[]), \
         patch("komit.generator.get_recent_commits", return_value=""):
        yield