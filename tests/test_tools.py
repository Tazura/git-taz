"""Tests for git-taz tools."""

from unittest.mock import Mock, patch

from src.git_taz.models import GitRepository, GitTool, ToolResult
from src.git_taz.tools import GitToolsManager


class TestGitToolsManager:
    """Test cases for the GitToolsManager class."""

    def test_init_with_repository(self) -> None:
        """Test initializing GitToolsManager with a repository."""
        repo = GitRepository.from_path(".")
        manager = GitToolsManager(repo)
        assert manager.repository == repo

    def test_get_tools_by_category(self) -> None:
        """Test getting tools organized by category."""
        repo = GitRepository.from_path(".")
        manager = GitToolsManager(repo)
        categories = manager.get_tools_by_category()

        assert isinstance(categories, dict)
        assert len(categories) > 0

        # Check that we have expected categories
        expected_categories = ["Information", "Maintenance"]
        for category in expected_categories:
            assert category in categories
            assert isinstance(categories[category], list)
            assert len(categories[category]) > 0

            # Check that all items are GitTool instances
            for tool in categories[category]:
                assert isinstance(tool, GitTool)
                assert tool.name
                assert tool.description
                assert tool.category == category

    @patch("subprocess.run")
    def test_git_status_success(self, mock_run: Mock) -> None:
        """Test successful git status execution."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="On branch main\nnothing to commit, working tree clean",
            stderr="",
        )

        repo = GitRepository.from_path(".")
        manager = GitToolsManager(repo)
        result = manager.git_status()

        assert isinstance(result, ToolResult)
        assert result.success is True
        assert result.output is not None
        assert "On branch main" in result.output
        assert result.error is None or result.error == ""

    @patch("subprocess.run")
    def test_git_status_failure(self, mock_run: Mock) -> None:
        """Test failed git status execution."""
        from subprocess import CalledProcessError

        mock_run.side_effect = CalledProcessError(
            1, ["git", "status", "--porcelain"], stderr="fatal: not a git repository"
        )

        repo = GitRepository.from_path(".")
        manager = GitToolsManager(repo)
        result = manager.git_status()

        assert isinstance(result, ToolResult)
        assert result.success is False
        assert result.error is not None
        assert "fatal: not a git repository" in result.error

    @patch("subprocess.run")
    def test_git_log_success(self, mock_run: Mock) -> None:
        """Test successful git log execution."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout=(
                "commit abc123\nAuthor: Test User\nDate: Today\n\n" "    Test commit"
            ),
            stderr="",
        )

        repo = GitRepository.from_path(".")
        manager = GitToolsManager(repo)
        result = manager.git_log()

        assert isinstance(result, ToolResult)
        assert result.success is True
        assert result.output is not None
        assert "commit abc123" in result.output

    @patch("subprocess.run")
    def test_git_branches_success(self, mock_run: Mock) -> None:
        """Test successful git branches execution."""
        mock_run.return_value = Mock(
            returncode=0, stdout="* main\n  develop\n  feature-branch", stderr=""
        )

        repo = GitRepository.from_path(".")
        manager = GitToolsManager(repo)
        result = manager.git_branches()

        assert isinstance(result, ToolResult)
        assert result.success is True
        assert result.output is not None
        assert "main" in result.output
        assert "develop" in result.output

    @patch("subprocess.run")
    def test_subprocess_exception(self, mock_run: Mock) -> None:
        """Test handling of subprocess exceptions."""
        mock_run.side_effect = OSError("Command failed")

        repo = GitRepository.from_path(".")
        manager = GitToolsManager(repo)
        result = manager.git_status()

        assert isinstance(result, ToolResult)
        assert result.success is False
        assert result.error is not None
        assert "Command failed" in result.error

    @patch("subprocess.run")
    def test_git_remotes_success(self, mock_run: Mock) -> None:
        """Test successful git remotes execution."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="origin\tupstream",
            stderr="",
        )

        repo = GitRepository.from_path(".")
        manager = GitToolsManager(repo)
        result = manager.git_remotes()

        assert isinstance(result, ToolResult)
        assert result.success is True
        assert result.output is not None
        assert "origin" in result.output

    @patch("subprocess.run")
    def test_git_diff_success(self, mock_run: Mock) -> None:
        """Test successful git diff execution."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="diff --git a/file.py b/file.py\n+added line",
            stderr="",
        )

        repo = GitRepository.from_path(".")
        manager = GitToolsManager(repo)
        result = manager.git_diff()

        assert isinstance(result, ToolResult)
        assert result.success is True
        assert result.output is not None
        assert "diff --git" in result.output

    @patch("subprocess.run")
    def test_git_gc_success(self, mock_run: Mock) -> None:
        """Test successful git gc execution."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="Counting objects: 100, done.",
            stderr="",
        )

        repo = GitRepository.from_path(".")
        manager = GitToolsManager(repo)
        result = manager.git_gc()

        assert isinstance(result, ToolResult)
        assert result.success is True
        assert result.output is not None
        assert "Counting objects" in result.output
