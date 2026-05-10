# tests/test_uninstall.py
import sys
from unittest.mock import patch, MagicMock


def test_uninstall_windows():
    mock_winreg = MagicMock()
    mock_winreg.OpenKey.return_value = MagicMock()
    mock_winreg.QueryValueEx.return_value = (r"C:\something;C:\Users\user\AppData\Local\komit", 0)

    with patch.dict(sys.modules, {"winreg": mock_winreg}):
        with patch("sys.platform", "win32"):
            with patch("os.path.exists", return_value=True):
                with patch("shutil.rmtree"):
                    with patch("subprocess.run"):
                        from komit import update_utils
                        update_utils.uninstall()

    mock_winreg.SetValueEx.assert_called_once()

def test_uninstall_linux():
    with patch("sys.platform", "linux"):
        with patch("os.path.exists", return_value=False):
            with patch("subprocess.run"):  # prevent actual git/rm commands
                with patch("shutil.rmtree"):  # prevent actual directory removal
                    from komit import update_utils
                    update_utils.uninstall()