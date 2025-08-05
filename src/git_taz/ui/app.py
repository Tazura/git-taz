"""Main Textual application for git-taz."""

from pathlib import Path
from typing import Optional

from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import DirectoryTree, Footer, Header, Log, OptionList, Static
from textual.widgets.option_list import Option

from ..models import GitRepository
from ..tools import GitToolsManager


class GitTazApp(App):
    """A Textual application for Git operations."""

    TITLE = "Git-Taz"
    SUB_TITLE = "Git Utility Tool"

    BINDINGS = [
        Binding("ctrl+c,ctrl+q", "quit", "Quit", show=True),
        Binding("ctrl+r", "refresh", "Refresh", show=True),
        Binding("ctrl+t", "toggle_sidebar", "Toggle Sidebar", show=True),
    ]

    CSS = """
    Screen {
        layout: horizontal;
    }
    
    #sidebar {
        width: 25%;
        dock: left;
        border: solid $primary;
    }
    
    #main {
        width: 75%;
        layout: vertical;
    }
    
    #tools_menu {
        height: 12;
        border: solid $accent;
        margin: 1 0;
    }
    
    #output {
        border: solid $success;
        margin: 1 0;
    }
    
    #repo_status {
        height: 3;
        border: solid $secondary;
        margin: 1 0;
    }
    """

    def __init__(self, repo_path: Optional[str] = None):
        """Initialize the app with an optional repository path."""
        super().__init__()
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.repository: Optional[GitRepository] = None
        self.tools_manager: Optional[GitToolsManager] = None
        self.sidebar_visible = True

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()

        with Container(id="sidebar"):
            yield Static("📁 Repository Browser", id="browser_title")
            yield DirectoryTree(str(self.repo_path), id="repo_tree")

            with Container(id="repo_status"):
                yield Static("📍 Repository", id="repo_title")
                yield Static("Loading...", id="repo_details")

        with Container(id="main"):
            with Container(id="tools_menu"):
                yield Static("🛠️  Git Tools", id="tools_title")
                yield OptionList(
                    Option("📊 Status", id="status"),
                    Option("📜 Log (Commits)", id="log"),
                    Option("🔍 Diff", id="diff"),
                    Option("🌳 Branches", id="branches"),
                    Option("🔗 Remotes", id="remotes"),
                    id="git_tools",
                )

            with Container(id="output"):
                yield Static("📄 Output", id="output_title")
                yield Log(id="command_log")

        yield Footer()

    def on_mount(self) -> None:
        """Called when app starts."""
        self.load_repository()

    def load_repository(self) -> None:
        """Load the Git repository."""
        try:
            self.repository = GitRepository.from_path(str(self.repo_path))
            self.tools_manager = GitToolsManager(self.repository)
            self.update_repo_info()
        except Exception as e:
            self.query_one("#repo_details", Static).update(f"Error: {e}")

    def update_repo_info(self) -> None:
        """Update the repository information display."""
        if self.repository and self.tools_manager:
            repo_name = self.repository.name
            git_status = "✅" if self.repository.is_git else "❌"

            info_text = Text()
            info_text.append(f"{repo_name} {git_status}\n", style="bold cyan")
            info_text.append(f"{self.repository.path}", style="dim")

            self.query_one("#repo_details", Static).update(info_text)

    def action_refresh(self) -> None:
        """Refresh the repository information."""
        self.load_repository()
        self.log_message("Repository refreshed", "info")

    def action_toggle_sidebar(self) -> None:
        """Toggle the sidebar visibility."""
        sidebar = self.query_one("#sidebar")
        if self.sidebar_visible:
            sidebar.styles.display = "none"
            self.query_one("#main").styles.width = "100%"
        else:
            sidebar.styles.display = "block"
            self.query_one("#main").styles.width = "70%"
        self.sidebar_visible = not self.sidebar_visible

    def log_message(self, message: str, level: str = "info") -> None:
        """Log a message to the output log."""
        log_widget = self.query_one("#command_log", Log)

        # Use simple color prefixes for now since Log widget style parameter doesn't work
        if level == "error":
            log_widget.write_line(f"🔴 {message}")
        elif level == "success":
            log_widget.write_line(f"✅ {message}")
        elif level == "warning":
            log_widget.write_line(f"⚠️  {message}")
        else:
            log_widget.write_line(f"ℹ️  {message}")

    async def run_git_tool(self, tool_name: str) -> None:
        """Run a Git tool and display the results."""
        if not self.tools_manager:
            self.log_message("No repository loaded", "error")
            return

        self.log_message(f"Running {tool_name}...", "info")

        try:
            # Map option IDs to tool methods with proper typing
            if tool_name == "status":
                result = self.tools_manager.git_status()
            elif tool_name == "log":
                # Use custom git log format for better commit display
                result = self.tools_manager.run_git_command(
                    [
                        "git",
                        "log",
                        "-n",
                        "15",
                        "--color",
                        "--graph",
                        "--abbrev-commit",
                        "--date=short",
                        "--pretty=format:%Cgreen%cd%Creset %C(bold blue)%<(22,trunc)%an%Creset %C(nobold red)%h%Creset %<(120,trunc)%s%C(bold yellow)%d%Creset%C(nobold nodim)",
                    ]
                )
            elif tool_name == "diff":
                result = self.tools_manager.git_diff()
            elif tool_name == "branches":
                result = self.tools_manager.git_branches()
            elif tool_name == "remotes":
                result = self.tools_manager.git_remotes()
            else:
                self.log_message(f"Unknown tool: {tool_name}", "error")
                return

            if result.success:
                self.log_message(f"✓ {tool_name} completed", "success")
                if result.output:
                    # For git log, display output line by line for better readability
                    if tool_name == "log":
                        self.log_message("📜 Recent Commits:", "info")
                        for line in result.output.split("\n"):
                            if line.strip():
                                self.log_message(line, "info")
                    else:
                        self.log_message(result.output, "info")
            else:
                self.log_message(f"✗ {tool_name} failed: {result.message}", "error")
                if result.error:
                    self.log_message(result.error, "error")

        except Exception as e:
            self.log_message(f"Error running {tool_name}: {e}", "error")

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle option selection from the tools menu."""
        option_id = event.option.id
        if option_id:
            self.run_worker(self.run_git_tool(option_id))

    def on_directory_tree_file_selected(self, event) -> None:
        """Handle file selection in the directory tree."""
        self.log_message(f"Selected: {event.path}", "info")


def run_app(repo_path: Optional[str] = None) -> None:
    """Run the Textual application."""
    app = GitTazApp(repo_path)
    app.run()
