"""Tests for git-taz core functionality."""

import pytest

from src.git_taz.core import greet, main


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

    def test_main_runs_without_error(self, capsys):
        """Test that main function runs without raising exceptions."""
        main()
        captured = capsys.readouterr()
        assert "Hello from git-taz!" in captured.out
