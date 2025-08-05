"""UI components for git-taz application."""

from typing import Optional

from .app import run_app


def run_ui(repo_path: Optional[str] = None) -> None:
    """Run the UI."""
    run_app(repo_path)
