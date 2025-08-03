"""Main application class for git-taz UI."""

from typing import Optional

import npyscreen

from ..models import GitRepository
from .repository_form import RepositorySelectForm
from .tool_selection_form import ToolSelectionForm


class GitTazApp(npyscreen.NPSAppManaged):
    """Main application class."""

    def __init__(self) -> None:
        super().__init__()
        self.repository: Optional[GitRepository] = None

    def onStart(self) -> None:
        """Initialize the application."""
        self.addForm("REPO_SELECT", RepositorySelectForm)
        self.addForm("MAIN", ToolSelectionForm)
        # Start with repository selection form
        self.setNextForm("REPO_SELECT")

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
