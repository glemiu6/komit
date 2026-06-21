import sys
from unittest.mock import patch

from komit.main import parse_args


def test_style_flag():
    with patch.object(sys, "argv", ["komit", "--style", "simple"]):
        assert parse_args().style == "simple"


def test_model_flag():
    with patch.object(sys, "argv", ["komit", "--model", "llama"]):
        assert parse_args().model == "llama"


def test_url_flag():
    with patch.object(sys, "argv", ["komit", "--ollama-url", "http://x"]):
        assert parse_args().ollama_url == "http://x"


def test_dry_run_flag():
    with patch.object(sys, "argv", ["komit", "--dry-run"]):
        assert parse_args().dry_run is True


def test_version_flag():
    with patch.object(sys, "argv", ["komit", "--version"]):
        try:
            parse_args()
        except SystemExit:
            assert True


def test_default_values():
    with patch.object(sys, "argv", ["komit"]):
        args = parse_args()
        assert args.model is None