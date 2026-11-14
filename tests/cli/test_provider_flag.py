"""CLI tests for the multi-provider configuration."""

import sys
from unittest.mock import patch

from komit.main import parse_args


def test_ollama_provider_flag():
    with patch.object(sys, "argv", ["komit", "--provider", "ollama"]):
        assert parse_args().provider == "ollama"


def test_openai_compatible_provider_flags():
    with patch.object(
        sys,
        "argv",
        ["komit", "--provider", "openai_compatible", "--base-url", "http://localhost:8080/v1"],
    ):
        args = parse_args()
    assert args.provider == "openai_compatible"
    assert args.base_url == "http://localhost:8080/v1"


def test_provider_defaults_are_delegated_to_config():
    with patch.object(sys, "argv", ["komit"]):
        args = parse_args()
    assert args.provider is None
    assert args.base_url is None
