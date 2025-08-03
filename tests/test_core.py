"""Tests for git-taz core functionality."""

from unittest.mock import patch

from src.git_taz.core import parse_arguments


class TestParseArguments:
    """Test cases for the parse_arguments function."""

    @patch("sys.argv", ["git-taz"])
    def test_parse_default_arguments(self) -> None:
        """Test parsing default arguments."""
        args = parse_arguments()
        assert args.repo == "."
        assert args.verbose is False

    @patch("sys.argv", ["git-taz", "--repo", "/path/to/repo"])
    def test_parse_repo_argument(self) -> None:
        """Test parsing repository argument."""
        args = parse_arguments()
        assert args.repo == "/path/to/repo"
        assert args.verbose is False

    @patch("sys.argv", ["git-taz", "-r", "/another/path"])
    def test_parse_repo_short_argument(self) -> None:
        """Test parsing repository short argument."""
        args = parse_arguments()
        assert args.repo == "/another/path"

    @patch("sys.argv", ["git-taz", "--verbose"])
    def test_parse_verbose_argument(self) -> None:
        """Test parsing verbose argument."""
        args = parse_arguments()
        assert args.verbose is True

    @patch("sys.argv", ["git-taz", "-v", "-r", "/test/path"])
    def test_parse_combined_arguments(self) -> None:
        """Test parsing combined arguments."""
        args = parse_arguments()
        assert args.repo == "/test/path"
        assert args.verbose is True
