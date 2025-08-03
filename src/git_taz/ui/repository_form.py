"""Repository selection form for git-taz application."""

import npyscreen

from ..models import GitRepository


class RepositorySelectForm(npyscreen.ActionForm):
    """Form to select or enter a repository path."""

    def create(self) -> None:
        """Create form widgets."""
        self.name = "Git-Taz: Repository Selection"
        self.repo_path = self.add(
            npyscreen.TitleText,
            name="Repository Path:",
            value=".",
        )
        self.status_display = self.add(
            npyscreen.Pager,
            name="Repository Status:",
            max_height=6,
            values=["Enter a repository path above and press OK to validate."],
        )

    def set_up_handlers(self) -> None:
        """Set up keyboard handlers."""
        super().set_up_handlers()
        # Add CTRL-C handler for exit
        self.handlers.update(
            {
                3: self._exit_app,  # CTRL-C
            }
        )

    def _exit_app(self, input) -> None:
        """Exit the application."""
        self.parentApp.setNextForm(None)
        self.parentApp.switchFormNow()

    def on_ok(self) -> None:
        """Handle OK button press."""
        repo_path = self.repo_path.value
        repository = GitRepository.from_path(repo_path)

        if not repository.exists:
            self.status_display.values = [
                f"Error: Path '{repo_path}' does not exist.",
                "Please enter a valid path.",
            ]
            self.status_display.display()
            return

        if not repository.is_git:
            self.status_display.values = [
                f"Error: '{repo_path}' is not a git repository.",
                "Please enter a path to a git repository.",
            ]
            self.status_display.display()
            return

        # Store repository in parent application
        self.parentApp.repository = repository
        self.parentApp.setNextForm("MAIN")

    def on_cancel(self) -> None:
        """Handle Cancel button press."""
        self.parentApp.setNextForm(None)
