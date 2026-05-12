import subprocess
from idlelib.iomenu import encoding

import pytest
from unittest.mock import patch, MagicMock
from komit.git_utils import (
    get_staged_diff,
    get_staged_files,
    commit,
    commit_with_editor,
    is_git_repo,
)


def _mock_run(stdout="", returncode=0):
    """Helper: return a mock CompletedProcess."""
    result = MagicMock()
    result.stdout = stdout
    result.returncode = returncode
    return result


class TestGetStagedDiff:
    @patch("komit.git_utils.subprocess.run")
    def test_returns_stdout(self, mock_run):
        mock_run.return_value = _mock_run(stdout="diff --git a/file.py b/file.py\n+new line")
        result = get_staged_diff()
        assert result == "diff --git a/file.py b/file.py\n+new line"

    @patch("komit.git_utils.subprocess.run")
    def test_calls_correct_git_command(self, mock_run):
        mock_run.return_value = _mock_run()
        get_staged_diff()
        mock_run.assert_called_once_with(
            ['git', 'diff', '--staged'],
            capture_output=True, text=True,encoding='utf-8',errors="replace"
        )

    @patch("komit.git_utils.subprocess.run")
    def test_returns_empty_string_when_nothing_staged(self, mock_run):
        mock_run.return_value = _mock_run(stdout="")
        result = get_staged_diff()
        assert result == ""


class TestGetStagedFiles:
    @patch("komit.git_utils.subprocess.run")
    def test_returns_list_of_files(self, mock_run):
        mock_run.return_value = _mock_run(stdout="src/auth.py\ntests/test_auth.py\nREADME.md\n")
        result = get_staged_files()
        assert result == ["src/auth.py", "tests/test_auth.py", "README.md"]

    @patch("komit.git_utils.subprocess.run")
    def test_returns_empty_list_when_nothing_staged(self, mock_run):
        mock_run.return_value = _mock_run(stdout="")
        result = get_staged_files()
        assert result == []

    @patch("komit.git_utils.subprocess.run")
    def test_filters_out_empty_strings(self, mock_run):
        mock_run.return_value = _mock_run(stdout="file1.py\n\nfile2.py\n")
        result = get_staged_files()
        assert "" not in result
        assert result == ["file1.py", "file2.py"]

    @patch("komit.git_utils.subprocess.run")
    def test_calls_correct_git_command(self, mock_run):
        mock_run.return_value = _mock_run()
        get_staged_files()
        mock_run.assert_called_once_with(
            ['git', 'diff', '--staged', '--name-only'],
            capture_output=True, text=True,encoding='utf-8'
        )

    @patch("komit.git_utils.subprocess.run")
    def test_single_file(self, mock_run):
        mock_run.return_value = _mock_run(stdout="main.py\n")
        result = get_staged_files()
        assert result == ["main.py"]


class TestCommit:
    @patch("komit.git_utils.subprocess.run")
    def test_calls_git_commit_with_message(self, mock_run):
        mock_run.return_value = _mock_run()
        commit("feat: add login")
        mock_run.assert_called_once_with(
            ['git', 'commit', '-m', 'feat: add login'],
            check=True,encoding='utf-8'
        )

    @patch("komit.git_utils.subprocess.run")
    def test_check_true_propagates_called_process_error(self, mock_run):
        """Fix #7: commit() must raise CalledProcessError on failure, not silently pass."""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'git commit')
        with pytest.raises(subprocess.CalledProcessError):
            commit("feat: will fail")

    @patch("komit.git_utils.subprocess.run")
    def test_message_with_special_characters(self, mock_run):
        mock_run.return_value = _mock_run()
        commit('fix: handle "quoted" values & symbols')
        call_args = mock_run.call_args[0][0]
        assert 'fix: handle "quoted" values & symbols' in call_args


class TestCommitWithEditor:
    @patch("komit.git_utils.subprocess.run")
    def test_calls_git_commit_with_edit_flag(self, mock_run):
        mock_run.return_value = _mock_run()
        commit_with_editor("feat: add login")
        mock_run.assert_called_once_with(
            ['git', 'commit', '-m', 'feat: add login', '-e'],
            check=True,encoding='utf-8',text=True
        )

    @patch("komit.git_utils.subprocess.run")
    def test_check_true_propagates_called_process_error(self, mock_run):
        """Fix #7: commit_with_editor() must also raise on failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'git commit')
        with pytest.raises(subprocess.CalledProcessError):
            commit_with_editor("feat: will fail")


class TestIsGitRepo:
    @patch("komit.git_utils.subprocess.run")
    def test_returns_true_when_inside_repo(self, mock_run):
        mock_run.return_value = _mock_run(returncode=0)
        assert is_git_repo() is True

    @patch("komit.git_utils.subprocess.run")
    def test_returns_false_when_outside_repo(self, mock_run):
        mock_run.return_value = _mock_run(returncode=128)
        assert is_git_repo() is False

    @patch("komit.git_utils.subprocess.run")
    def test_calls_correct_git_command(self, mock_run):
        mock_run.return_value = _mock_run()
        is_git_repo()
        mock_run.assert_called_once_with(
            ['git', 'rev-parse', '--is-inside-work-tree'],
            capture_output=True, text=True,encoding='utf-8'
        )