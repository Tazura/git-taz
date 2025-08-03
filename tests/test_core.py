"""Tests for git-taz core functionality."""

from unittest.mock import patch

from src.git_taz.core import main, parse_arguments


class TestMain:
    """Test cases for the main function."""

    @patch("src.git_taz.ui.run_ui")
    @patch("sys.argv", ["git-taz"])
    def test_main_default(self, mock_run_ui):
        """Test main function with default arguments."""
        main()
        mock_run_ui.assert_called_once_with(None)

    @patch("src.git_taz.ui.run_ui")
    @patch("sys.argv", ["git-taz", "--repo", "/path/to/repo"])
    def test_main_with_repo_path(self, mock_run_ui):
        """Test main function with repository path."""
        main()
        mock_run_ui.assert_called_once_with("/path/to/repo")

    @patch("src.git_taz.ui.run_ui")
    @patch("sys.argv", ["git-taz", "--repo", "."])
    def test_main_with_current_directory(self, mock_run_ui):
        """Test main function with current directory as repo."""
        main()
        mock_run_ui.assert_called_once_with(None)


class TestParseArguments:
    """Test cases for the parse_arguments function."""

    @patch("sys.argv", ["git-taz"])
    def test_parse_default_arguments(self):
        """Test parsing default arguments."""
        args = parse_arguments()
        assert args.repo == "."
        assert args.verbose is False

    @patch("sys.argv", ["git-taz", "--repo", "/path/to/repo"])
    def test_parse_repo_argument(self):
        """Test parsing repository argument."""
        args = parse_arguments()
        assert args.repo == "/path/to/repo"
        assert args.verbose is False

    @patch("sys.argv", ["git-taz", "-r", "/another/path"])
    def test_parse_repo_short_argument(self):
        """Test parsing repository short argument."""
        args = parse_arguments()
        assert args.repo == "/another/path"

    @patch("sys.argv", ["git-taz", "--verbose"])
    def test_parse_verbose_argument(self):
        """Test parsing verbose argument."""
        args = parse_arguments()
        assert args.verbose is True

    @patch("sys.argv", ["git-taz", "-v", "-r", "/test/path"])
    def test_parse_combined_arguments(self):
        """Test parsing combined arguments."""
        args = parse_arguments()
        assert args.repo == "/test/path"
        assert args.verbose is True
