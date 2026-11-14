from unittest.mock import patch

import pytest

from komit.generator import generate_message


@patch("komit.generator._create_checked_provider")
def test_invalid_model_response_does_not_get_committed(mock_provider_factory):
    provider = mock_provider_factory.return_value

    provider.generate.return_value = "Here is the commit message: feat: update"

    with pytest.raises(RuntimeError, match="Conventional Commit"):
        generate_message("diff")

    provider.generate.assert_called_once()
