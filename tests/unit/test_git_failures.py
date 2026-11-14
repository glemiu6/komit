import subprocess
from unittest.mock import patch

import pytest

from komit.git_utils import get_staged_diff, get_staged_files


@pytest.mark.parametrize("read_staged", [get_staged_diff, get_staged_files])
def test_staged_git_failure_is_not_silent(read_staged):
    failure = subprocess.CalledProcessError(128, ["git", "diff", "--staged"])
    with patch("komit.git_utils.subprocess.run", side_effect=failure):
        with pytest.raises(subprocess.CalledProcessError):
            read_staged()
