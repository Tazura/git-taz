"""Command selection form for git-taz application."""

import npyscreen


class CommandSelectionForm(npyscreen.ActionFormMinimal):
    """Form to select available commands."""

    def create(self) -> None:
        """Create form widgets."""
        self.name = "Git-Taz: Command Selection"

        # Current command display
        self.current_command = self.add(
            npyscreen.FixedText,
            name="Current command:",
            value="Select repository",
            editable=False,
        )

        self.add(npyscreen.FixedText, value="", editable=False)  # Spacer

        # Available commands
        self.command_list = self.add(
            npyscreen.MultiLineAction,
            name="Available Commands:",
            values=[
                "Select repository",
                "Tool selection",
                "Exit",
            ],
            max_height=8,
        )
        self.command_list.actionHighlighted = self.command_selected

        # Status bar
        self.add(npyscreen.FixedText, value="", editable=False)  # Spacer
        self.status_bar = self.add(
            npyscreen.FixedText,
            value="Enter: Select | CTRL-C: Exit | ESC: Cancel",
            editable=False,
        )

    def set_up_handlers(self) -> None:
        """Set up keyboard handlers."""
        super().set_up_handlers()
        # Add CTRL-C handler for exit
        self.handlers.update(
            {
                3: self._exit_app,  # CTRL-C
                27: self._cancel,  # ESC
            }
        )

    def _exit_app(self, input) -> None:
        """Exit the application."""
        self.parentApp.setNextForm(None)
        self.parentApp.switchFormNow()

    def _cancel(self, input) -> None:
        """Cancel and return to previous form."""
        # Return to the form that was active before command selection
        if hasattr(self.parentApp, "previous_form"):
            self.parentApp.setNextForm(self.parentApp.previous_form)
        else:
            self.parentApp.setNextForm("MAIN")
        self.parentApp.switchFormNow()

    def command_selected(self, line_index: int, line_value: str) -> None:
        """Handle command selection."""
        command = self.command_list.values[line_index]

        if command == "Select repository":
            self.parentApp.setNextForm("REPO_SELECT")
            self.parentApp.switchFormNow()
        elif command == "Tool selection":
            if hasattr(self.parentApp, "repository") and self.parentApp.repository:
                self.parentApp.setNextForm("MAIN")
                self.parentApp.switchFormNow()
            else:
                # Show message that repository must be selected first
                npyscreen.notify_confirm(
                    "Please select a repository first before accessing tools.",
                    title="No Repository Selected",
                )
        elif command == "Exit":
            self.parentApp.setNextForm(None)
            self.parentApp.switchFormNow()
