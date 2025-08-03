"""Main application class for git-taz UI."""

from typing import Optional

import npyscreen

from ..models import GitRepository
from .command_selection_form import CommandSelectionForm
from .repository_form import RepositorySelectForm
from .tool_selection_form import ToolSelectionForm


class GitTazApp(npyscreen.NPSAppManaged):
    """Main application class."""

    def __init__(self) -> None:
        super().__init__()
        self.repository: Optional[GitRepository] = None
        self.previous_form: Optional[str] = None

        # Try to initialize with current directory if it's a git repo
        self._initialize_repository()

    def _initialize_repository(self) -> None:
        """Initialize repository from current directory if it's a git repo."""
        current_dir = "."
        try:
            repo = GitRepository.from_path(current_dir)
            if repo.exists and repo.is_git:
                self.repository = repo
        except Exception:
            # If there's any error, just leave repository as None
            pass

    def onStart(self) -> None:
        """Initialize the application."""
        self.addForm("REPO_SELECT", RepositorySelectForm)
        self.addForm("MAIN", ToolSelectionForm)
        self.addForm("COMMAND_SELECT", CommandSelectionForm)
        # Start with the main form (tool selection)
        self.setNextForm("MAIN")

    def onInMainLoop(self) -> None:
        """Called during main loop - handle global shortcuts."""
        # This allows us to handle CTRL-C at the application level
        pass

    def while_waiting(self) -> None:
        """Handle global keyboard shortcuts."""
        # Handle CTRL-C globally
        try:
            # This will be called periodically
            pass
        except KeyboardInterrupt:
            self.setNextForm(None)
