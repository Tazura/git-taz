"""Data models for git-taz application."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class GitRepository:
    """Represents a Git repository."""

    path: str
    name: str
    exists: bool
    is_git: bool
    absolute_path: str

    @classmethod
    def from_path(cls, repo_path: str) -> "GitRepository":
        """Create a GitRepository instance from a path."""
        repo = Path(repo_path)
        repo_absolute = repo.absolute()

        return cls(
            path=repo_path,
            name=repo_absolute.name,
            exists=repo.exists(),
            is_git=cls._is_git_repository(repo),
            absolute_path=str(repo_absolute),
        )

    @staticmethod
    def _is_git_repository(repo: Path) -> bool:
        """Check if a path is a git repository."""
        if not repo.exists() or not repo.is_dir():
            return False
        git_dir = repo / ".git"
        return git_dir.exists()


@dataclass
class GitTool:
    """Represents a git tool/command."""

    name: str
    description: str
    category: str
    enabled: bool = True


@dataclass
class ToolResult:
    """Represents the result of running a tool."""

    success: bool
    message: str
    output: Optional[str] = None
    error: Optional[str] = None
