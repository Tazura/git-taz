"""Data models for git-taz application."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import git


@dataclass
class GitRepository:
    """Represents a Git repository using GitPython."""

    path: str
    name: str
    exists: bool
    is_git: bool
    absolute_path: str
    repo: Optional[git.Repo] = field(default=None, repr=False)

    @classmethod
    def from_path(cls, repo_path: str) -> "GitRepository":
        repo_path_obj = Path(repo_path)
        repo_absolute = repo_path_obj.absolute()
        exists = repo_path_obj.exists()
        is_git = False
        repo = None
        try:
            repo = git.Repo(str(repo_absolute))
            is_git = True
        except (git.exc.InvalidGitRepositoryError, git.exc.NoSuchPathError):
            repo = None
            is_git = False
        return cls(
            path=repo_path,
            name=repo_absolute.name,
            exists=exists,
            is_git=is_git,
            absolute_path=str(repo_absolute),
            repo=repo,
        )


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
