"""Tool selection form for git-taz application."""

from typing import Dict, Optional

import npyscreen

from ..models import GitTool, ToolResult
from ..tools import GitToolsManager


class ToolSelectionForm(npyscreen.ActionFormMinimal):
    """Main form for tool selection and execution."""

    def create(self) -> None:
        """Create form widgets."""
        self.name = "Git-Taz: Tool Selection"

        # Repository info
        self.repo_info = self.add(
            npyscreen.FixedText, name="Repository:", value="", editable=False
        )

        self.add(npyscreen.FixedText, value="", editable=False)  # Spacer

        # Tool categories - leave space for output and status bar
        self.tool_list = self.add(
            npyscreen.MultiLineAction, name="Available Tools:", values=[], max_height=8
        )
        self.tool_list.actionHighlighted = self.tool_selected

        # Output area - reduce max_height to leave space for status bar
        self.add(npyscreen.FixedText, value="", editable=False)  # Spacer
        self.output_area = self.add(
            npyscreen.Pager,
            name="Output:",
            max_height=5,
            values=["Select a tool above to see its output here."],
        )

        # Status bar at the bottom
        self.add(npyscreen.FixedText, value="", editable=False)  # Spacer
        self.status_bar = self.add(
            npyscreen.FixedText,
            value="F2: Commands | CTRL-H: Help | CTRL-X/CTRL-C: Exit",
            editable=False,
        )

    def while_waiting(self) -> None:
        """Handle keyboard shortcuts while waiting for input."""
        # This method is called when the form is waiting for input
        pass

    def set_up_handlers(self) -> None:
        """Set up keyboard handlers."""
        super().set_up_handlers()
        # Add custom key handlers
        self.handlers.update(
            {
                # ord("^H"): self._show_help,  # CTRL-H
                8: self._show_help,  # CTRL-H (backspace)
                # ord("^X"): self._exit_app,  # CTRL-X
                24: self._exit_app,  # CTRL-X
                # ord("^C"): self._exit_app,  # CTRL-C
                3: self._exit_app,  # CTRL-C
                # CTRL-A for command selection
                1: self._show_commands,  # CTRL-A
            }
        )

    def _exit_app(self, input) -> None:
        """Exit the application."""
        self.parentApp.setNextForm(None)
        self.parentApp.switchFormNow()

    def _select_repo(self, input) -> None:
        """Switch to repository selection."""
        self.parentApp.setNextForm("REPO_SELECT")
        self.parentApp.switchFormNow()

    def _show_commands(self, input) -> None:
        """Show command selection dialog."""
        self.parentApp.previous_form = "MAIN"
        self.parentApp.setNextForm("COMMAND_SELECT")
        self.parentApp.switchFormNow()

    def _show_help(self, input=None) -> None:
        """Show help dialog."""
        help_text = [
            "Git-Taz Help",
            "=============",
            "",
            "Navigation:",
            "- Use arrow keys or Tab/Shift+Tab to move between widgets",
            "- Enter/Space: Select a tool to execute",
            "",
            "Keyboard Shortcuts:",
            "- F2: Show command selection",
            "- CTRL-H: Show this help",
            "- CTRL-X or CTRL-C: Exit application",
            "",
            "Tool Categories:",
            "- Information: Get repository status and information",
            "- Maintenance: Perform repository maintenance tasks",
            "",
            "Press any key to continue...",
        ]

        # Create a simple form for help display
        help_form = npyscreen.ActionPopup(
            name="Help",
            lines=20,
            columns=60,
        )
        help_form.preserve_selected_widget = True

        # Add a multiline widget to display help text
        help_form.add(
            npyscreen.Pager,
            values=help_text,
            max_height=-2,
        )

        # Show the form
        help_form.edit()

    def beforeEditing(self) -> None:
        """Called before the form is displayed."""
        if hasattr(self.parentApp, "repository") and self.parentApp.repository:
            repo = self.parentApp.repository
            self.repo_info.value = f"{repo.name} ({repo.absolute_path})"
            self._load_tools()
        else:
            self.repo_info.value = "No repository selected"
            # Clear tools if no repository
            self.tool_list.values = [
                "No repository selected.",
                "Press F2 to select a command or repository.",
            ]
            self.output_area.values = [
                "Select a repository first to see available tools."
            ]

    def _load_tools(self) -> None:
        """Load tools organized by category."""
        tools_manager = GitToolsManager(self.parentApp.repository)
        categories = tools_manager.get_tools_by_category()

        tool_items = []
        self.tool_mapping: Dict[int, Optional[GitTool]] = {}

        for category, tools in categories.items():
            tool_items.append(f"=== {category} ===")
            self.tool_mapping[len(tool_items) - 1] = None  # Category header

            for tool in tools:
                tool_items.append(f"  {tool.name} - {tool.description}")
                self.tool_mapping[len(tool_items) - 1] = tool

        self.tool_list.values = tool_items
        self.tools_manager = tools_manager

    def tool_selected(self, line_index: int, line_value: str) -> None:
        """Handle tool selection."""
        if line_index not in self.tool_mapping:
            return

        tool = self.tool_mapping[line_index]
        if tool is None:  # Category header
            return

        self.output_area.values = [f"Executing {tool.name}..."]
        self.output_area.display()

        # Execute the tool
        result = self._execute_tool(tool)

        # Display result
        output_lines = [f"=== {tool.name} ==="]
        if result.success:
            if result.output:
                output_lines.extend(result.output.split("\n"))
            else:
                output_lines.append("Command completed successfully (no output)")
        else:
            output_lines.append(f"Error: {result.message}")
            if result.error:
                output_lines.extend(result.error.split("\n"))

        self.output_area.values = output_lines
        self.output_area.display()

    def _execute_tool(self, tool: GitTool) -> ToolResult:
        """Execute a selected tool."""
        # Map tool names to methods
        tool_methods = {
            "Git Status": self.tools_manager.git_status,
            "Git Log": self.tools_manager.git_log,
            "List Branches": self.tools_manager.git_branches,
            "List Remotes": self.tools_manager.git_remotes,
            "Git Diff": self.tools_manager.git_diff,
            "Git GC": self.tools_manager.git_gc,
        }

        method = tool_methods.get(tool.name)
        if method:
            return method()
        else:
            return ToolResult(
                success=False, message=f"Tool '{tool.name}' not implemented yet"
            )
