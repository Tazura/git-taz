"""Main Textual application for git-taz."""

from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.command import Hit, Hits, Provider
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import (
    Button,
    DataTable,
    DirectoryTree,
    Footer,
    Header,
    Log,
    Select,
    Static,
)

from ..models import GitRepository
from ..services import GitOperationsService
from ..tools import GitToolsManager


class GitToolsProvider(Provider):
    """A command provider for Git tools."""

    async def startup(self) -> None:
        """Called once when the command palette is opened."""
        pass

    async def search(self, query: str) -> Hits:
        """Search for Git tool commands."""
        matcher = self.matcher(query)

        # Define your Git tools
        tools = [
            ("status", "Show working tree status"),
            ("log", "Show commit history"),
            ("branches", "List branches"),
            ("diff", "Show file differences"),
        ]

        for tool_id, description in tools:
            command = f"git {tool_id}"
            score = matcher.match(command)
            if score > 0:

                def make_tool_runner(tool: str):
                    def run_tool():
                        from typing import cast

                        app = cast("GitTazApp", self.app)
                        app._execute_git_tool(tool)

                    return run_tool

                yield Hit(
                    score,
                    matcher.highlight(command),
                    make_tool_runner(tool_id),
                    help=description,
                )


class GitTazApp(App):
    """A Textual application for Git operations."""

    TITLE = "Git-Taz"
    SUB_TITLE = "Git Utility Tool"

    BINDINGS = [
        Binding("ctrl+c,ctrl+q", "quit", "Quit", show=True),
        Binding("ctrl+r", "refresh", "Refresh", show=True),
        Binding("ctrl+t", "toggle_sidebar", "Toggle Sidebar", show=True),
        Binding("ctrl+b", "checkout", "Checkout Branch/Tag", show=True),
    ]

    # Add the custom Git tools provider to the command palette
    COMMANDS = App.COMMANDS | {GitToolsProvider}

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

    #commits_panel {
        height: 70%;
        border: solid $success;
        margin: 1 0;
    }

    #output_panel {
        height: 30%;
        border: solid $warning;
        margin: 1 0;
    }

    .repo_info {
        background: $primary 20%;
        color: $text;
        padding: 1;
        margin: 1 0;
    }

    .checkout-dialog {
        align: center middle;
        width: 50%;
        height: 50%;
        border: tall $primary;
        background: $background;
        padding: 2;
    }

    .checkout-dialog Select {
        margin: 1;
    }

    .checkout-dialog .dialog-title {
        text-align: center;
        color: $primary;
        dock: top;
        border-bottom: tall $primary;
    }
    """

    def __init__(self, repo_path: Optional[str] = None):
        """Initialize the app with an optional repository path."""
        super().__init__()
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.repository: Optional[GitRepository] = None
        self.tools_manager: Optional[GitToolsManager] = None
        self.git_operations: Optional[GitOperationsService] = None
        self.sidebar_visible = True

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()

        with Container(id="sidebar"):
            yield Static("Repository Info", classes="repo_info")
            yield Static("Loading...", id="repo_details")
            yield Static("Files", id="files_title")
            yield DirectoryTree(str(self.repo_path), id="repo_tree")

        with Container(id="main"):
            with Container(id="commits_panel"):
                yield Static("Commit History", id="commits_title")
                yield DataTable(id="commits_table")

            with Container(id="output_panel"):
                yield Static("Output", id="output_title")
                yield Log(id="command_log")

        yield Footer()

    def on_mount(self) -> None:
        """Called when app starts."""
        self.setup_commits_table()
        self.load_repository()

    def setup_commits_table(self) -> None:
        """Setup the commits table with columns."""
        table = self.query_one("#commits_table", DataTable)
        table.add_columns("Date", "Author", "Hash", "Message", "Refs")
        table.cursor_type = "row"

    def load_repository(self) -> None:
        """Load the Git repository."""
        try:
            self.repository = GitRepository.from_path(str(self.repo_path))
            self.tools_manager = GitToolsManager(self.repository)
            self.git_operations = GitOperationsService(self.repository)
            self.update_repo_info()
            self.load_commits()
        except Exception as e:
            self.query_one("#repo_details", Static).update(f"Error: {e}")

    def update_repo_info(self) -> None:
        """Update the repository information display."""
        if self.repository and self.repository.repo:
            try:
                current_branch = self.repository.repo.active_branch.name
                self.sub_title = f"Git Utility Tool - {current_branch}"

                repo_text = Text()
                repo_text.append(f"📁 {self.repository.name}\n", style="bold cyan")
                repo_text.append(f"🌿 {current_branch}\n", style="green")
                repo_text.append(f"📍 {self.repository.path}", style="dim")

                self.query_one("#repo_details", Static).update(repo_text)
            except Exception:
                self.sub_title = "Git Utility Tool"
                repo_text = Text()
                repo_text.append(f"📁 {self.repository.name}\n", style="bold cyan")
                repo_text.append("❌ No Git repo", style="red")
                self.query_one("#repo_details", Static).update(repo_text)

    def load_commits(self) -> None:
        """Load commit history into the table."""
        if not self.repository or not self.repository.repo:
            return

        table = self.query_one("#commits_table", DataTable)
        table.clear()

        try:
            # Get commits using your preferred format
            commits = list(self.repository.repo.iter_commits("HEAD", max_count=15))

            for commit in commits:
                # Format date
                commit_date = datetime.fromtimestamp(commit.committed_date).strftime(
                    "%Y-%m-%d %H:%M"
                )

                # Format author (truncate to 22 chars)
                author_name = commit.author.name or "Unknown"
                author = author_name[:22] if len(author_name) > 22 else author_name

                # Format hash (abbreviated)
                short_hash = str(commit.hexsha)[:7]

                # Format message (truncate to 80 chars)
                commit_message = str(commit.message)
                message_lines = commit_message.strip().split("\n")
                message = message_lines[0] if message_lines else ""
                if len(message) > 80:
                    message = message[:77] + "..."

                # Format refs (branches, tags)
                refs = ""
                try:
                    refs_list = []
                    for ref in self.repository.repo.refs:
                        if ref.commit == commit:
                            refs_list.append(ref.name.split("/")[-1])
                    if refs_list:
                        refs = f"({', '.join(refs_list)})"
                except Exception:
                    pass

                table.add_row(commit_date, author, short_hash, message, refs)

        except Exception as e:
            self.log_message(f"Error loading commits: {e}", "error")

    def action_refresh(self) -> None:
        """Refresh the repository information."""
        self.load_repository()
        self.log_message("Repository refreshed", "info")

    def action_toggle_sidebar(self) -> None:
        """Toggle the sidebar visibility."""
        sidebar = self.query_one("#sidebar")
        main_panel = self.query_one("#main")
        if self.sidebar_visible:
            sidebar.styles.display = "none"
            main_panel.styles.width = "100%"
        else:
            sidebar.styles.display = "block"
            main_panel.styles.width = "75%"
        self.sidebar_visible = not self.sidebar_visible

    def log_message(self, message: str, level: str = "info") -> None:
        """Log a message to the output log."""
        log_widget = self.query_one("#command_log", Log)

        # Use emoji prefixes for visual distinction
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
        if not self.git_operations:
            self.log_message("No repository loaded", "error")
            return

        self.log_message(f"Running git {tool_name}...", "info")

        try:
            if tool_name == "status":
                result = self.git_operations.get_status()
            elif tool_name == "log":
                result = self.git_operations.get_log()
            elif tool_name == "branches":
                result = self.git_operations.get_branches_info()
            elif tool_name == "diff":
                result = self.git_operations.get_diff()
            else:
                self.log_message(f"Unknown tool: {tool_name}", "error")
                return

            if result.success:
                self.log_message(f"✓ git {tool_name} completed", "success")
                if result.output:
                    # Split long output into multiple lines
                    lines = result.output.split("\n")
                    for line in lines[:20]:  # Limit to first 20 lines
                        if line.strip():
                            self.log_message(line.strip(), "info")
                    if len(lines) > 20:
                        self.log_message(f"... ({len(lines) - 20} more lines)", "info")
            else:
                self.log_message(f"✗ git {tool_name} failed: {result.message}", "error")
                if result.error:
                    self.log_message(result.error, "error")

        except Exception as e:
            self.log_message(f"Error running git {tool_name}: {e}", "error")

    def _execute_git_tool(self, tool_name: str) -> None:
        """Execute a git tool from the command palette."""
        self.run_worker(self.run_git_tool(tool_name))

    class CheckoutScreen(Screen):
        """Screen for selecting branches/tags to checkout."""

        def __init__(self, git_operations: GitOperationsService, parent_app):
            super().__init__()
            self.git_operations = git_operations
            self.parent_app = parent_app

        def compose(self) -> ComposeResult:
            yield Vertical(
                Static("Checkout Branch/Tag", classes="dialog-title"),
                Select(
                    [
                        ("Branches", "branches"),
                        ("Tags", "tags"),
                    ],
                    prompt="Select type",
                    id="type_select",
                    value="branches",
                ),
                Select([], prompt="Select branch/tag", id="target_select"),
                Horizontal(
                    Button("Checkout", id="checkout_button", variant="primary"),
                    Button("Cancel", id="cancel_button", variant="default"),
                    classes="centered-buttons",
                ),
                classes="checkout-dialog",
            )

        def on_mount(self) -> None:
            self.update_targets("branches")

        def on_select_changed(self, message: Select.Changed) -> None:
            if message.select.id == "type_select":
                if message.value:
                    self.update_targets(str(message.value))

        def update_targets(self, target_type: str) -> None:
            target_select = self.query_one("#target_select", Select)
            targets = self.git_operations.get_checkout_targets(target_type)
            target_select.set_options(targets)

        def on_button_pressed(self, message: Button.Pressed) -> None:
            if message.button.id == "checkout_button":
                target_select = self.query_one("#target_select", Select)
                selected_target = target_select.value

                if selected_target:
                    result = self.git_operations.checkout(str(selected_target))
                    if result.success:
                        self.parent_app.log_message(result.message, "success")
                        self.parent_app.load_repository()  # Refresh the UI
                        self.dismiss()
                    else:
                        self.parent_app.log_message(result.message, "error")
                else:
                    self.parent_app.log_message("No target selected", "warning")

            elif message.button.id == "cancel_button":
                self.dismiss()

    def action_checkout(self) -> None:
        """Open a dialog to checkout a branch or tag."""
        if not self.git_operations:
            self.log_message("No repository loaded", "error")
            return

        checkout_screen = self.CheckoutScreen(self.git_operations, self)
        self.push_screen(checkout_screen)

    def on_directory_tree_file_selected(self, event) -> None:
        """Handle file selection in the directory tree."""
        self.log_message(f"Selected: {event.path}", "info")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle commit selection in the table."""
        table = event.data_table
        row_key = event.row_key
        row_data = table.get_row(row_key)
        commit_hash = row_data[2]  # Hash is in the 3rd column
        self.log_message(f"Selected commit: {commit_hash}", "info")


def run_app(repo_path: Optional[str] = None) -> None:
    """Run the Textual application."""
    app = GitTazApp(repo_path)
    app.run()
