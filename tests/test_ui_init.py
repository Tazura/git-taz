"""Tests for git-taz UI initialization."""

from unittest.mock import Mock, patch

from src.git_taz.ui import run_ui


class TestRunUI:
    """Test cases for the run_ui function."""

    @patch("src.git_taz.ui.GitTazApp")
    def test_run_ui_no_repo_path(self, mock_app: Mock) -> None:
        """Test run_ui without repository path."""
        mock_app_instance = Mock()
        mock_app.return_value = mock_app_instance

        run_ui()

        mock_app.assert_called_once()
        mock_app_instance.run.assert_called_once()

    @patch("src.git_taz.models.GitRepository.from_path")
    @patch("src.git_taz.ui.GitTazApp")
    def test_run_ui_with_repo_path(self, mock_app: Mock, mock_from_path: Mock) -> None:
        """Test run_ui with repository path."""
        mock_app_instance = Mock()
        mock_app.return_value = mock_app_instance

        mock_repo = Mock()
        mock_repo.exists = True
        mock_repo.is_git = True
        mock_from_path.return_value = mock_repo

        run_ui("/path/to/repo")

        mock_from_path.assert_called_once_with("/path/to/repo")
        assert mock_app_instance.repository == mock_repo
        mock_app_instance.run.assert_called_once()

    @patch("src.git_taz.models.GitRepository.from_path")
    @patch("src.git_taz.ui.GitTazApp")
    def test_run_ui_with_invalid_repo(
        self, mock_app: Mock, mock_from_path: Mock
    ) -> None:
        """Test run_ui with invalid repository path."""
        mock_app_instance = Mock()
        mock_app.return_value = mock_app_instance

        mock_from_path.side_effect = Exception("Not a git repository")

        run_ui("/invalid/path")

        # Should handle exception gracefully
        mock_app_instance.run.assert_called_once()

    @patch("src.git_taz.ui.GitTazApp")
    def test_run_ui_keyboard_interrupt(self, mock_app: Mock) -> None:
        """Test run_ui handles KeyboardInterrupt."""
        mock_app_instance = Mock()
        mock_app_instance.run.side_effect = KeyboardInterrupt()
        mock_app.return_value = mock_app_instance

        # Should not raise exception
        run_ui()

        mock_app_instance.run.assert_called_once()

    @patch("src.git_taz.ui.GitTazApp")
    @patch("locale.setlocale")
    def test_run_ui_locale_fallback(self, mock_setlocale: Mock, mock_app: Mock) -> None:
        """Test run_ui locale fallback behavior."""
        # Simulate locale errors
        import locale

        mock_setlocale.side_effect = [
            locale.Error("Locale not available"),
            locale.Error("UTF-8 not available"),
            None,  # Success on third call (C locale)
        ]

        mock_app_instance = Mock()
        mock_app.return_value = mock_app_instance

        run_ui()

        # Should have tried multiple locale settings
        assert mock_setlocale.call_count >= 2
        mock_app_instance.run.assert_called_once()
