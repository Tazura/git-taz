"""Tests for git-taz models."""

import tempfile
from pathlib import Path

from src.git_taz.models import GitRepository, GitTool, ToolResult


class TestGitRepository:
    """Test cases for the GitRepository class."""

    def test_from_path_existing_git_repo(self) -> None:
        """Test creating GitRepository from existing git repository."""
        # Assuming the project root is a git repository
        repo = GitRepository.from_path(".")
        assert repo.absolute_path == str(Path(".").absolute())
        assert repo.name == Path(".").absolute().name
        assert repo.exists is True
        # This will be True if run from within a git repository
        assert isinstance(repo.is_git, bool)

    def test_from_path_nonexistent_path(self) -> None:
        """Test creating GitRepository from non-existent path."""
        repo = GitRepository.from_path("/nonexistent/path")
        assert "/nonexistent/path" in repo.absolute_path
        assert repo.name == "path"
        assert repo.exists is False
        assert repo.is_git is False

    def test_from_path_with_relative_path(self) -> None:
        """Test creating GitRepository from relative path."""
        repo = GitRepository.from_path("./")
        assert repo.absolute_path == str(Path("./").absolute())
        assert repo.exists is True

    def test_from_path_with_tempdir(self) -> None:
        """Test creating GitRepository from temporary directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = GitRepository.from_path(temp_dir)
            assert repo.absolute_path == temp_dir
            assert repo.exists is True
            assert repo.is_git is False  # temp dir is not a git repo


class TestGitTool:
    """Test cases for the GitTool class."""

    def test_git_tool_creation(self) -> None:
        """Test creating a GitTool instance."""
        tool = GitTool(name="Test Tool", description="A test tool", category="Testing")
        assert tool.name == "Test Tool"
        assert tool.description == "A test tool"
        assert tool.category == "Testing"
        assert tool.enabled is True

    def test_git_tool_creation_disabled(self) -> None:
        """Test creating a disabled GitTool instance."""
        tool = GitTool(
            name="Disabled Tool",
            description="A disabled tool",
            category="Testing",
            enabled=False,
        )
        assert tool.name == "Disabled Tool"
        assert tool.enabled is False


class TestToolResult:
    """Test cases for the ToolResult class."""

    def test_successful_result(self) -> None:
        """Test creating a successful ToolResult."""
        result = ToolResult(
            success=True, message="Success", output="Command output", error=None
        )
        assert result.success is True
        assert result.output == "Command output"
        assert result.error is None
        assert result.message == "Success"

    def test_failed_result(self) -> None:
        """Test creating a failed ToolResult."""
        result = ToolResult(
            success=False, message="Command failed", output=None, error="Error message"
        )
        assert result.success is False
        assert result.output is None
        assert result.error == "Error message"
        assert result.message == "Command failed"

    def test_result_with_minimal_info(self) -> None:
        """Test creating ToolResult with minimal information."""
        result = ToolResult(success=True, message="Done")
        assert result.success is True
        assert result.output is None
        assert result.error is None
        assert result.message == "Done"
