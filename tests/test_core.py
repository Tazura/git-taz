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
        assert args.command is None

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

    @patch("sys.argv", ["git-taz", "checkout", "main"])
    def test_parse_checkout_command(self):
        """Test parsing checkout command."""
        args = parse_arguments()
        assert args.command == "checkout"
        assert args.target == "main"
        assert args.interactive is False
        assert args.list_branches is False
        assert args.list_tags is False

    @patch("sys.argv", ["git-taz", "checkout", "--interactive"])
    def test_parse_checkout_interactive(self):
        """Test parsing checkout command with interactive flag."""
        args = parse_arguments()
        assert args.command == "checkout"
        assert args.interactive is True

    @patch("sys.argv", ["git-taz", "checkout", "--list-branches"])
    def test_parse_checkout_list_branches(self):
        """Test parsing checkout command with list branches flag."""
        args = parse_arguments()
        assert args.command == "checkout"
        assert args.list_branches is True

    @patch("sys.argv", ["git-taz", "checkout", "--list-tags"])
    def test_parse_checkout_list_tags(self):
        """Test parsing checkout command with list tags flag."""
        args = parse_arguments()
        assert args.command == "checkout"
        assert args.list_tags is True


class TestMainCLI:
    """Test cases for CLI command handling in main function."""

    @patch("src.git_taz.cli.CheckoutCLI")
    @patch("sys.argv", ["git-taz", "checkout", "--list-branches"])
    def test_main_checkout_list_branches(self, mock_checkout_cli):
        """Test main function with checkout list branches command."""
        mock_cli_instance = mock_checkout_cli.return_value
        
        main()
        
        mock_checkout_cli.assert_called_once_with(None)
        mock_cli_instance.list_branches.assert_called_once()

    @patch("src.git_taz.cli.CheckoutCLI")
    @patch("sys.argv", ["git-taz", "checkout", "--list-tags"])
    def test_main_checkout_list_tags(self, mock_checkout_cli):
        """Test main function with checkout list tags command."""
        mock_cli_instance = mock_checkout_cli.return_value
        
        main()
        
        mock_checkout_cli.assert_called_once_with(None)
        mock_cli_instance.list_tags.assert_called_once()

    @patch("src.git_taz.cli.CheckoutCLI")
    @patch("sys.argv", ["git-taz", "checkout", "--interactive"])
    def test_main_checkout_interactive(self, mock_checkout_cli):
        """Test main function with checkout interactive command."""
        mock_cli_instance = mock_checkout_cli.return_value
        
        main()
        
        mock_checkout_cli.assert_called_once_with(None)
        mock_cli_instance.checkout_interactive.assert_called_once()

    @patch("src.git_taz.cli.CheckoutCLI")
    @patch("sys.argv", ["git-taz", "checkout", "main"])
    def test_main_checkout_direct(self, mock_checkout_cli):
        """Test main function with direct checkout command."""
        mock_cli_instance = mock_checkout_cli.return_value
        
        main()
        
        mock_checkout_cli.assert_called_once_with(None)
        mock_cli_instance.checkout_direct.assert_called_once_with("main")

    @patch("src.git_taz.cli.CheckoutCLI")
    @patch("sys.argv", ["git-taz", "-r", "/path/to/repo", "checkout"])
    def test_main_checkout_with_repo_path(self, mock_checkout_cli):
        """Test main function with checkout command and repo path."""
        mock_cli_instance = mock_checkout_cli.return_value
        
        main()
        
        mock_checkout_cli.assert_called_once_with("/path/to/repo")
        mock_cli_instance.checkout_interactive.assert_called_once()
