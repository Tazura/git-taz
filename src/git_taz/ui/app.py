"""Main Textual application for git-taz."""

from pathlib import Path
from typing import Optional

from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.widgets import Button, DirectoryTree, Footer, Header, Log, Static

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
        width: 30%;
        dock: left;
        border: solid $primary;
    }
    
    #main {
        width: 70%;
        margin: 1;
    }
    
    #repo_info {
        height: 4;
        border: solid $secondary;
    }
    
    #tools {
        height: 8;
        border: solid $accent;
    }
    
    #output {
        border: solid $success;
    }
    
    .tool_button {
        margin: 1;
        min-width: 15;
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
            yield Static("Repository Browser", id="browser_title")
            yield DirectoryTree(str(self.repo_path), id="repo_tree")

        with Container(id="main"):
            with Container(id="repo_info"):
                yield Static("Repository Information", id="repo_title")
                yield Static("Loading...", id="repo_details")

            with Container(id="tools"):
                yield Static("Git Tools", id="tools_title")
                with Horizontal():
                    yield Button("Status", id="btn_status", classes="tool_button")
                    yield Button("Log", id="btn_log", classes="tool_button")
                    yield Button("Diff", id="btn_diff", classes="tool_button")
                with Horizontal():
                    yield Button("Branches", id="btn_branches", classes="tool_button")
                    yield Button("Remotes", id="btn_remotes", classes="tool_button")

            with Container(id="output"):
                yield Static("Output", id="output_title")
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
            info_text = Text()
            info_text.append(f"Path: {self.repository.path}\n", style="cyan")
            info_text.append(f"Name: {self.repository.name}\n", style="green")
            info_text.append(
                f"Git Repo: {'Yes' if self.repository.is_git else 'No'}\n",
                style="yellow",
            )
            info_text.append(
                f"Exists: {'Yes' if self.repository.exists else 'No'}", style="blue"
            )

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
            # Map button IDs to tool methods with proper typing
            if tool_name == "btn_status":
                result = self.tools_manager.git_status()
            elif tool_name == "btn_log":
                result = self.tools_manager.git_log()
            elif tool_name == "btn_diff":
                result = self.tools_manager.git_diff()
            elif tool_name == "btn_branches":
                result = self.tools_manager.git_branches()
            elif tool_name == "btn_remotes":
                result = self.tools_manager.git_remotes()
            else:
                self.log_message(f"Unknown tool: {tool_name}", "error")
                return

            if result.success:
                self.log_message(f"✓ {tool_name} completed", "success")
                if result.output:
                    self.log_message(result.output, "info")
            else:
                self.log_message(f"✗ {tool_name} failed: {result.message}", "error")
                if result.error:
                    self.log_message(result.error, "error")

        except Exception as e:
            self.log_message(f"Error running {tool_name}: {e}", "error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        button_id = event.button.id
        if button_id and button_id.startswith("btn_"):
            # Create a task for the async method
            self.run_worker(self.run_git_tool(button_id))

    def on_directory_tree_file_selected(self, event) -> None:
        """Handle file selection in the directory tree."""
        self.log_message(f"Selected: {event.path}", "info")


def run_app(repo_path: Optional[str] = None) -> None:
    """Run the Textual application."""
    app = GitTazApp(repo_path)
    app.run()
