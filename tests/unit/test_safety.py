import subprocess
import sys
from unittest.mock import patch

import pytest

from komit.komitconfig import KomitConfig
from komit.main import run


def test_staged_diff_change_prevents_commit(capsys):
    with (
        patch.object(sys, "argv", ["komit"]),
        patch("komit.main.check_for_updates"),
        patch("komit.main.is_git_repo", return_value=True),
        patch("komit.main.get_staged_diff", side_effect=["original diff", "new diff"]),
        patch("komit.main.get_staged_files", return_value=["code.py"]),
        patch("komit.main.get_current_branch", return_value="feature/test"),
        patch("komit.main.KomitConfig.from_sources", return_value=KomitConfig()),
        patch("komit.main.generate_message", return_value=("feat: change", [])),
        patch("komit.main.Prompt.ask", return_value="y"),
        patch("komit.main.commit") as commit,
    ):
        with pytest.raises(SystemExit) as exc:
            run()

    assert exc.value.code == 1
    commit.assert_not_called()
    assert "Staged changes have changed" in capsys.readouterr().out


def test_git_error_is_not_reported_as_empty_staging(capsys):
    with (
        patch.object(sys, "argv", ["komit"]),
        patch("komit.main.check_for_updates"),
        patch("komit.main.is_git_repo", return_value=True),
        patch(
            "komit.main.get_staged_diff",
            side_effect=subprocess.CalledProcessError(128, ["git", "diff"]),
        ),
    ):
        with pytest.raises(SystemExit) as exc:
            run()

    assert exc.value.code == 1
    assert "Could not read staged changes" in capsys.readouterr().out
