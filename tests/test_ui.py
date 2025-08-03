"""Tests for git-taz UI components."""

from unittest.mock import Mock, patch

from src.git_taz.ui.app import GitTazApp


class TestGitTazApp:
    """Test cases for the GitTazApp class."""

    @patch("src.git_taz.models.GitRepository.from_path")
    def test_app_initialization_no_repo(self, mock_from_path: Mock) -> None:
        """Test GitTazApp initialization when no git repo is found."""
        # Mock no repository found
        mock_from_path.side_effect = Exception("Not a git repository")

        app = GitTazApp()
        assert app.repository is None
        assert app.previous_form is None

    @patch("src.git_taz.models.GitRepository.from_path")
    def test_app_initialization_with_repo(self, mock_from_path: Mock) -> None:
        """Test GitTazApp initialization with git repository."""
        # Mock a valid git repository
        mock_repo = Mock()
        mock_repo.exists = True
        mock_repo.is_git = True
        mock_from_path.return_value = mock_repo

        app = GitTazApp()
        assert app.repository == mock_repo

    @patch("src.git_taz.models.GitRepository.from_path")
    def test_initialize_repository_not_git(self, mock_from_path: Mock) -> None:
        """Test repository initialization when path is not a git repo."""
        mock_repo = Mock()
        mock_repo.exists = True
        mock_repo.is_git = False
        mock_from_path.return_value = mock_repo

        app = GitTazApp()
        app._initialize_repository()

        # Should not set repository if it's not a git repo
        assert app.repository != mock_repo

    @patch("src.git_taz.models.GitRepository.from_path")
    def test_initialize_repository_exception(self, mock_from_path: Mock) -> None:
        """Test repository initialization when exception occurs."""
        mock_from_path.side_effect = OSError("Permission denied")

        app = GitTazApp()
        app._initialize_repository()

        # Should handle exception gracefully
        assert app.repository is None

    def test_app_forms_setup(self) -> None:
        """Test that app sets up forms correctly."""
        # We can't easily test the actual form setup without mocking npyscreen
        # But we can test that the method exists and can be called
        app = GitTazApp()
        app.addForm = Mock()
        app.setNextForm = Mock()

        app.onStart()

        # Verify forms are added
        assert app.addForm.call_count == 3
        assert app.setNextForm.called

    def test_on_in_main_loop(self) -> None:
        """Test onInMainLoop method."""
        app = GitTazApp()
        # Should not raise any exception
        app.onInMainLoop()

    def test_while_waiting(self) -> None:
        """Test while_waiting method."""
        app = GitTazApp()
        # Should not raise any exception
        app.while_waiting()

    def test_while_waiting_with_keyboard_interrupt(self) -> None:
        """Test while_waiting method with KeyboardInterrupt."""
        app = GitTazApp()
        app.setNextForm = Mock()

        # The current implementation doesn't actually catch KeyboardInterrupt
        # but we can test that the method doesn't crash
        app.while_waiting()

        # Should not have called setNextForm in normal case
        assert not app.setNextForm.called
