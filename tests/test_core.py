"""Tests for git-taz core functionality."""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from src.git_taz.core import (
    get_repository_info,
    greet,
    main,
    parse_arguments,
    validate_git_repository,
)


class TestGreet:
    """Test cases for the greet function."""

    def test_greet_default(self):
        """Test greet with default parameter."""
        result = greet()
        assert result == "Hello from git-taz!"

    def test_greet_with_name(self):
        """Test greet with custom name."""
        result = greet("World")
        assert result == "Hello from World!"

    def test_greet_empty_string(self):
        """Test greet with empty string."""
        result = greet("")
        assert result == "Hello from !"

    @pytest.mark.parametrize(
        "name,expected",
        [
            ("Alice", "Hello from Alice!"),
            ("Bob", "Hello from Bob!"),
            ("123", "Hello from 123!"),
            ("test-name", "Hello from test-name!"),
        ],
    )
    def test_greet_parametrized(self, name, expected):
        """Test greet with various names."""
        result = greet(name)
        assert result == expected


class TestMain:
    """Test cases for the main function."""

    @patch("sys.argv", ["git-taz", "--repo", "."])
    def test_main_with_current_directory(self, capsys):
        """Test main function with current directory as repo."""
        # This test assumes the test is run from a git repository
        main()
        captured = capsys.readouterr()
        assert "Hello from git-taz processing" in captured.out

    @patch("sys.argv", ["git-taz", "--repo", "/nonexistent"])
    def test_main_with_invalid_repo(self, capsys):
        """Test main function with invalid repository path."""
        main()
        captured = capsys.readouterr()
        assert "Error:" in captured.out
        assert "is not a valid git repository" in captured.out


class TestValidateGitRepository:
    """Test cases for the validate_git_repository function."""

    def test_validate_current_directory(self):
        """Test validation of current directory (should be a git repo)."""
        # Assuming tests are run from the project root which is a git repo
        result = validate_git_repository(".")
        assert result is True

    def test_validate_nonexistent_directory(self):
        """Test validation of non-existent directory."""
        result = validate_git_repository("/nonexistent/path")
        assert result is False

    def test_validate_non_git_directory(self):
        """Test validation of directory that's not a git repository."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = validate_git_repository(temp_dir)
            assert result is False

    def test_validate_file_instead_of_directory(self):
        """Test validation when path points to a file instead of directory."""
        with tempfile.NamedTemporaryFile() as temp_file:
            result = validate_git_repository(temp_file.name)
            assert result is False


class TestGetRepositoryInfo:
    """Test cases for the get_repository_info function."""

    def test_get_info_current_directory(self):
        """Test getting repository info for current directory."""
        result = get_repository_info(".")
        assert "path" in result
        assert "name" in result
        assert "exists" in result
        assert "is_git" in result
        assert result["exists"] is True

    def test_get_info_nonexistent_directory(self):
        """Test getting repository info for non-existent directory."""
        result = get_repository_info("/nonexistent/path")
        assert result["exists"] is False
        assert result["is_git"] is False


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
