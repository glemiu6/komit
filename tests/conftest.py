"""
Shared pytest fixtures for the komit test suite.
"""
import pytest
from komit.komitconfig import KomitConfig


@pytest.fixture
def default_config():
    return KomitConfig()


@pytest.fixture
def simple_config():
    return KomitConfig(style="simple")


@pytest.fixture
def detailed_config():
    return KomitConfig(style="detailed")


@pytest.fixture
def small_diff_limit_config():
    """Config with a very small diff limit — useful for truncation tests."""
    return KomitConfig(max_diff_length=50)


@pytest.fixture
def sample_diff():
    return (
        "diff --git a/komit/main.py b/komit/main.py\n"
        "index 1234567..abcdefg 100644\n"
        "--- a/komit/main.py\n"
        "+++ b/komit/main.py\n"
        "@@ -1,3 +1,5 @@\n"
        "+import sys\n"
        " def run():\n"
        "+    print('hello')\n"
        "     pass\n"
    )


@pytest.fixture
def large_diff():
    """A diff that exceeds the default max_diff_length of 4000 chars."""
    return "+" + "x" * 5000


@pytest.fixture
def staged_files():
    return ["komit/main.py", "tests/test_main.py"]