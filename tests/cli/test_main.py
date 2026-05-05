import subprocess
import pytest
from unittest.mock import patch
from komit.main import run
import sys


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _patch_all(
    is_repo=True,
    diff="diff content",
    files=["file.py"],
    message="feat: add thing",
    inputs=None,
):
    """
    Context manager stack that patches all external dependencies of run().
    `inputs` is a list of strings simulating successive user inputs.
    """
    import contextlib

    patches = [
        patch("komit.main.is_git_repo", return_value=is_repo),
        patch("komit.main.get_staged_diff", return_value=diff),
        patch("komit.main.get_staged_files", return_value=files),
        patch("komit.main.generate_message", return_value=message),
        patch("komit.main.commit"),
        patch("komit.main.commit_with_editor"),
    ]
    if inputs is not None:
        patches.append(patch("builtins.input", side_effect=inputs))

    return contextlib.ExitStack(), patches


# ---------------------------------------------------------------------------
# Tests: early exit conditions
# ---------------------------------------------------------------------------

class TestRunEarlyExits:
    @patch("komit.main.is_git_repo", return_value=False)
    def test_exits_when_not_a_git_repo(self, _, capsys):
        with patch.object(sys, "argv", ["komit"]):  # add this
            with pytest.raises(SystemExit) as exc:
                run()
            assert exc.value.code == 1

    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="")
    def test_exits_when_no_staged_changes(self, _diff, _repo, capsys):
        with pytest.raises(SystemExit) as exc:
            run()
        assert exc.value.code == 1
        assert "No staged changes" in capsys.readouterr().out

    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="some diff")
    @patch("komit.main.get_staged_files", return_value=["file.py"])
    @patch("komit.main.generate_message", side_effect=RuntimeError("Ollama not running"))
    def test_exits_on_generate_failure(self, _gen, _files, _diff, _repo, capsys):
        with pytest.raises(SystemExit) as exc:
            run()
        assert exc.value.code == 1
        assert "Ollama not running" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Tests: output formatting
# ---------------------------------------------------------------------------

class TestRunOutput:
    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="diff")
    @patch("komit.main.get_staged_files", return_value=["a.py", "b.py"])
    @patch("komit.main.generate_message", return_value="feat: something")
    @patch("komit.main.commit")
    @patch("builtins.input", return_value="y")
    def test_staged_files_label_is_correct(self, _in, _commit, _gen, _files, _diff, _repo, capsys):
        """Fix #2: must print 'Staged files' not 'Stage files'."""
        run()
        out = capsys.readouterr().out
        assert "Staged files (2):" in out

    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="diff")
    @patch("komit.main.get_staged_files", return_value=["file.py"])
    @patch("komit.main.generate_message", return_value="feat: something")
    @patch("komit.main.commit")
    @patch("builtins.input", return_value="y")
    def test_each_file_is_listed(self, _in, _commit, _gen, _files, _diff, _repo, capsys):
        run()
        out = capsys.readouterr().out
        assert "  - file.py" in out

    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="diff")
    @patch("komit.main.get_staged_files", return_value=["file.py"])
    @patch("komit.main.generate_message", return_value="feat: add thing")
    @patch("komit.main.commit")
    @patch("builtins.input", return_value="y")
    def test_suggested_message_is_printed(self, _in, _commit, _gen, _files, _diff, _repo, capsys):
        run()
        out = capsys.readouterr().out
        assert "feat: add thing" in out


# ---------------------------------------------------------------------------
# Tests: user choices
# ---------------------------------------------------------------------------

class TestRunChoiceY:
    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="diff")
    @patch("komit.main.get_staged_files", return_value=["file.py"])
    @patch("komit.main.generate_message", return_value="feat: thing")
    @patch("komit.main.commit")
    @patch("builtins.input", return_value="y")
    def test_y_calls_commit(self, _in, mock_commit, _gen, _files, _diff, _repo):
        run()
        mock_commit.assert_called_once_with("feat: thing")

    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="diff")
    @patch("komit.main.get_staged_files", return_value=["file.py"])
    @patch("komit.main.generate_message", return_value="feat: thing")
    @patch("komit.main.commit")
    @patch("builtins.input", return_value="y")
    def test_y_prints_committed(self, _in, _commit, _gen, _files, _diff, _repo, capsys):
        """Fix #3: must print 'Committed!' not 'Commited!'."""
        run()
        assert "Committed!" in capsys.readouterr().out

    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="diff")
    @patch("komit.main.get_staged_files", return_value=["file.py"])
    @patch("komit.main.generate_message", return_value="feat: thing")
    @patch("komit.main.commit", side_effect=subprocess.CalledProcessError(1, "git"))
    @patch("builtins.input", return_value="y")
    def test_y_exits_if_commit_fails(self, _in, _commit, _gen, _files, _diff, _repo):
        with pytest.raises(SystemExit) as exc:
            run()
        assert exc.value.code == 1


class TestRunChoiceN:
    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="diff")
    @patch("komit.main.get_staged_files", return_value=["file.py"])
    @patch("komit.main.generate_message", return_value="feat: thing")
    @patch("komit.main.commit")
    @patch("builtins.input", return_value="n")
    def test_n_does_not_commit(self, _in, mock_commit, _gen, _files, _diff, _repo):
        run()
        mock_commit.assert_not_called()

    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="diff")
    @patch("komit.main.get_staged_files", return_value=["file.py"])
    @patch("komit.main.generate_message", return_value="feat: thing")
    @patch("komit.main.commit")
    @patch("builtins.input", return_value="n")
    def test_n_prints_cancelled(self, _in, _commit, _gen, _files, _diff, _repo, capsys):
        run()
        assert "cancelled" in capsys.readouterr().out.lower()


class TestRunChoiceE:
    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="diff")
    @patch("komit.main.get_staged_files", return_value=["file.py"])
    @patch("komit.main.generate_message", return_value="feat: thing")
    @patch("komit.main.commit_with_editor")
    @patch("builtins.input", return_value="e")
    def test_e_calls_commit_with_editor(self, _in, mock_editor, _gen, _files, _diff, _repo):
        run()
        mock_editor.assert_called_once_with("feat: thing")

    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="diff")
    @patch("komit.main.get_staged_files", return_value=["file.py"])
    @patch("komit.main.generate_message", return_value="feat: thing")
    @patch("komit.main.commit_with_editor", side_effect=subprocess.CalledProcessError(1, "git"))
    @patch("builtins.input", return_value="e")
    def test_e_exits_if_editor_commit_fails(self, _in, _editor, _gen, _files, _diff, _repo):
        with pytest.raises(SystemExit) as exc:
            run()
        assert exc.value.code == 1


class TestRunChoiceR:
    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="diff")
    @patch("komit.main.get_staged_files", return_value=["file.py"])
    @patch("komit.main.commit")
    @patch("builtins.input", side_effect=["r", "y"])
    def test_r_regenerates_then_y_commits(self, _in, mock_commit, _files, _diff, _repo):
        """Fix #5: regenerate path must not crash and must loop back correctly."""
        with patch("komit.main.generate_message", side_effect=["feat: first", "feat: second"]) as mock_gen:
            run()
        assert mock_gen.call_count == 2
        mock_commit.assert_called_once_with("feat: second")

    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="diff")
    @patch("komit.main.get_staged_files", return_value=["file.py"])
    @patch("komit.main.commit")
    @patch("builtins.input", side_effect=["r", "n"])
    def test_r_then_n_cancels(self, _in, mock_commit, _files, _diff, _repo):
        with patch("komit.main.generate_message", side_effect=["feat: first", "feat: second"]):
            run()
        mock_commit.assert_not_called()

    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="diff")
    @patch("komit.main.get_staged_files", return_value=["file.py"])
    @patch("builtins.input", side_effect=["r", "n"])
    def test_r_exits_if_regenerate_fails(self, _in, _files, _diff, _repo):
        """Fix #5: RuntimeError during regenerate must exit cleanly."""
        with patch("komit.main.generate_message", side_effect=[
            "feat: first",
            RuntimeError("Ollama crashed"),
        ]):
            with pytest.raises(SystemExit) as exc:
                run()
        assert exc.value.code == 1

    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="diff")
    @patch("komit.main.get_staged_files", return_value=["file.py"])
    @patch("komit.main.generate_message", return_value="feat: thing")
    @patch("komit.main.commit")
    @patch("builtins.input", side_effect=["r", "y"])
    def test_r_prints_new_suggested_message(self, _in, _commit, _gen, _files, _diff, _repo, capsys):
        run()
        assert "New suggested message" in capsys.readouterr().out


class TestRunChoiceInvalid:
    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="diff")
    @patch("komit.main.get_staged_files", return_value=["file.py"])
    @patch("komit.main.generate_message", return_value="feat: thing")
    @patch("komit.main.commit")
    @patch("builtins.input", side_effect=["z", "y"])
    def test_invalid_input_shows_error_and_loops(self, _in, mock_commit, _gen, _files, _diff, _repo, capsys):
        """Fix #6: unknown input must print a message and loop, not silently continue."""
        run()
        out = capsys.readouterr().out
        assert "Invalid choice" in out
        mock_commit.assert_called_once()

    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="diff")
    @patch("komit.main.get_staged_files", return_value=["file.py"])
    @patch("komit.main.generate_message", return_value="feat: thing")
    @patch("komit.main.commit")
    @patch("builtins.input", side_effect=["", "  ", "Y", "y"])
    def test_case_insensitive_input(self, _in, mock_commit, _gen, _files, _diff, _repo):
        """Input is lowercased, so 'Y' should work the same as 'y'."""
        run()
        mock_commit.assert_called_once()


class TestRunCLIArgs:
    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="diff")
    @patch("komit.main.get_staged_files", return_value=["file.py"])
    @patch("komit.main.commit")
    @patch("builtins.input", return_value="n")
    def test_default_style_is_conventional(self, _in, _commit, _files, _diff, _repo):
        with patch("komit.main.generate_message", return_value="feat: thing") as mock_gen:
            run()  # conftest.py reset_argv already sets sys.argv = ["komit"]
        call_config = mock_gen.call_args.kwargs["config"]
        assert call_config.style == "conventional"

    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="diff")
    @patch("komit.main.get_staged_files", return_value=["file.py"])
    @patch("komit.main.commit")
    @patch("builtins.input", return_value="n")
    def test_style_flag_simple(self, _in, _commit, _files, _diff, _repo):
        with patch("komit.main.generate_message", return_value="Add thing") as mock_gen:
            with patch.object(sys, "argv", ["komit", "--style", "simple"]):
                run()
        call_config = mock_gen.call_args.kwargs["config"]
        assert call_config.style == "simple"

    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="diff")
    @patch("komit.main.get_staged_files", return_value=["file.py"])
    @patch("komit.main.commit")
    @patch("builtins.input", return_value="n")
    def test_style_flag_detailed(self, _in, _commit, _files, _diff, _repo):
        with patch("komit.main.generate_message", return_value="feat: thing") as mock_gen:
            import sys
            with patch.object(sys, "argv", ["komit", "--style", "detailed"]):
                run()
            call_config = mock_gen.call_args.kwargs["config"]
            assert call_config.style == "detailed"

    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="diff")
    @patch("komit.main.get_staged_files", return_value=["file.py"])
    @patch("komit.main.commit")
    @patch("builtins.input", return_value="n")
    def test_model_flag(self, _in, _commit, _files, _diff, _repo):
        with patch("komit.main.generate_message", return_value="feat: thing") as mock_gen:
            import sys
            with patch.object(sys, "argv", ["komit", "--model", "llama3.2:3b"]):
                run()
            call_config = mock_gen.call_args.kwargs["config"]
            assert call_config.model == "llama3.2:3b"

    @patch("komit.main.is_git_repo", return_value=True)
    @patch("komit.main.get_staged_diff", return_value="diff")
    @patch("komit.main.get_staged_files", return_value=["file.py"])
    @patch("komit.main.commit")
    @patch("builtins.input", return_value="n")
    def test_ollama_url_flag(self, _in, _commit, _files, _diff, _repo):
        with patch("komit.main.generate_message", return_value="feat: thing") as mock_gen:
            import sys
            with patch.object(sys, "argv", ["komit", "--ollama-url", "http://remotehost:11434"]):
                run()
            call_config = mock_gen.call_args.kwargs["config"]
            assert call_config.ollama_url == "http://remotehost:11434"