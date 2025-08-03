"""UI components for git-taz application."""

import locale
import os
from typing import Any, Optional

# Fix locale issues before importing npyscreen
os.environ.setdefault("LANG", "C.UTF-8")
os.environ.setdefault("LC_ALL", "C.UTF-8")

# Patch locale.setlocale to handle errors gracefully
_original_setlocale = locale.setlocale


def _patched_setlocale(category: int, locale_name: Optional[str] = None) -> str:
    """Patched setlocale that falls back to C locale on errors."""
    try:
        if locale_name == "":
            # Try common fallbacks for empty locale string
            for fallback in ["C.UTF-8", "en_US.UTF-8", "C"]:
                try:
                    return _original_setlocale(category, fallback)
                except locale.Error:
                    continue
            # If all fallbacks fail, use C
            return _original_setlocale(category, "C")
        else:
            return _original_setlocale(category, locale_name)
    except locale.Error:
        # Final fallback to C locale
        return _original_setlocale(category, "C")


# Apply the patch
locale.setlocale = _patched_setlocale

import npyscreen  # noqa: E402

from ..models import GitRepository, GitTool, ToolResult  # noqa: E402
from ..tools import GitToolsManager  # noqa: E402


class RepositorySelectForm(npyscreen.ActionForm):
    """Form to select or enter a repository path."""

    def create(self):
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

    def on_ok(self):
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

    def on_cancel(self):
        """Handle Cancel button press."""
        self.parentApp.setNextForm(None)


class ToolSelectionForm(npyscreen.ActionFormMinimal):
    """Main form for tool selection and execution."""

    def create(self):
        """Create form widgets."""
        self.name = "Git-Taz: Tool Selection"

        # Repository info
        self.repo_info = self.add(
            npyscreen.FixedText, name="Repository:", value="", editable=False
        )

        self.add(npyscreen.FixedText, value="", editable=False)  # Spacer

        # Tool categories - reduce max_height to leave space for output
        self.tool_list = self.add(
            npyscreen.MultiLineAction, name="Available Tools:", values=[], max_height=10
        )
        self.tool_list.actionHighlighted = self.tool_selected

        # Output area - reduce max_height
        self.add(npyscreen.FixedText, value="", editable=False)  # Spacer
        self.output_area = self.add(
            npyscreen.Pager,
            name="Output:",
            max_height=6,
            values=["Select a tool above to see its output here."],
        )

    def beforeEditing(self):
        """Called before the form is displayed."""
        if hasattr(self.parentApp, "repository") and self.parentApp.repository:
            repo = self.parentApp.repository
            self.repo_info.value = f"{repo.name} ({repo.absolute_path})"
            self._load_tools()
        else:
            self.repo_info.value = "No repository selected"

    def _load_tools(self):
        """Load tools organized by category."""
        tools_manager = GitToolsManager(self.parentApp.repository)
        categories = tools_manager.get_tools_by_category()

        tool_items = []
        self.tool_mapping = {}  # Map display index to tool info

        for category, tools in categories.items():
            tool_items.append(f"=== {category} ===")
            self.tool_mapping[len(tool_items) - 1] = None  # Category header

            for tool in tools:
                tool_items.append(f"  {tool.name} - {tool.description}")
                self.tool_mapping[len(tool_items) - 1] = tool

        self.tool_list.values = tool_items
        self.tools_manager = tools_manager

    def tool_selected(self, line_index, line_value):
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


class GitTazApp(npyscreen.NPSAppManaged):
    """Main application class."""

    def __init__(self):
        super().__init__()
        self.repository: Optional[GitRepository] = None

    def onStart(self):
        """Initialize the application."""
        self.addForm("REPO_SELECT", RepositorySelectForm)
        self.addForm("MAIN", ToolSelectionForm)


def run_ui() -> None:
    """Run the npyscreen UI."""
    # Fix locale issues that can occur in some environments
    try:
        locale.setlocale(locale.LC_ALL, "")
    except locale.Error:
        # Fallback to C locale if system locale is not available
        try:
            locale.setlocale(locale.LC_ALL, "C.UTF-8")
        except locale.Error:
            locale.setlocale(locale.LC_ALL, "C")

    # Set environment variable to prevent ncurses locale issues
    os.environ.setdefault("LANG", "en_US.UTF-8")

    try:
        app = GitTazApp()
        app.run()
    except KeyboardInterrupt:
        pass  # Clean exit on Ctrl+C
