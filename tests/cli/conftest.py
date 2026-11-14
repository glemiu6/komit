# tests/cli/conftest.py
import sys
from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def reset_argv():
    with patch.object(sys, "argv", ["komit"]):
        yield


@pytest.fixture(autouse=True)
def no_update_check():
    with patch("komit.update_utils.check_for_updates"):
        yield


@pytest.fixture(autouse=True)
def isolate_config(tmp_path):
    """Prevent tests from reading or writing the real config file."""
    with patch(
        "komit.config_utils.get_default_config_path", return_value=str(tmp_path / "config.toml")
    ):
        yield
