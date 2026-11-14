import sys
from unittest.mock import patch

import pytest

from komit.main import parse_args


def test_branch_false():
    with patch.object(sys, "argv", ["komit", "--include_branch_name", "false"]):
        assert parse_args().include_branch_name is False


def test_branch_true():
    with patch.object(sys, "argv", ["komit", "--include-branch-name", "true"]):
        assert parse_args().include_branch_name is True


def test_branch_negative_flag():
    with patch.object(sys, "argv", ["komit", "--no-include-branch-name"]):
        assert parse_args().include_branch_name is False


def test_branch_invalid_value():
    with patch.object(sys, "argv", ["komit", "--include_branch_name", "perhaps"]):
        with pytest.raises(SystemExit):
            parse_args()
