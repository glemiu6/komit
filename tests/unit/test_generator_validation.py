from unittest.mock import MagicMock, patch

import pytest

from komit.generator import generate_message


@patch("komit.generator.model_exist", return_value=True)
@patch("komit.generator.check_ollama_running", return_value=True)
@patch("ollama.Client")
def test_invalid_model_response_does_not_get_committed(mock_client, _running, _model):
    response = MagicMock()
    response.message.content = "Here is the commit message: feat: update"
    mock_client.return_value.chat.return_value = response
    with pytest.raises(RuntimeError, match="Conventional Commit"):
        generate_message("diff")
