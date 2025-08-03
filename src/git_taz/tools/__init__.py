"""Git tools and utilities."""

import subprocess
from typing import Dict, List

from ..models import GitRepository, GitTool, ToolResult


class GitToolsManager:
    """Manages git tools and operations."""

    def __init__(self, repository: GitRepository):
        self.repository = repository
        self._tools = self._initialize_tools()

    def _initialize_tools(self) -> Dict[str, GitTool]:
        """Initialize available git tools."""
        return {
            "status": GitTool(
                name="Git Status",
                description="Show the working tree status",
                category="Information",
            ),
            "log": GitTool(
                name="Git Log", description="Show commit logs", category="Information"
            ),
            "branches": GitTool(
                name="List Branches",
                description="List all branches",
                category="Information",
            ),
            "remotes": GitTool(
                name="List Remotes",
                description="List remote repositories",
                category="Information",
            ),
            "diff": GitTool(
                name="Git Diff",
                description="Show changes between commits",
                category="Analysis",
            ),
            "blame": GitTool(
                name="Git Blame",
                description="Show revision and author for each line",
                category="Analysis",
            ),
            "clean": GitTool(
                name="Git Clean",
                description="Remove untracked files from working tree",
                category="Maintenance",
            ),
            "gc": GitTool(
                name="Git GC",
                description="Cleanup unnecessary files and optimize repo",
                category="Maintenance",
            ),
        }

    def get_tools_by_category(self) -> Dict[str, List[GitTool]]:
        """Get tools organized by category."""
        categories: Dict[str, List[GitTool]] = {}
        for tool in self._tools.values():
            if tool.category not in categories:
                categories[tool.category] = []
            categories[tool.category].append(tool)
        return categories

    def get_all_tools(self) -> List[GitTool]:
        """Get all available tools."""
        return list(self._tools.values())

    def run_git_command(self, command: List[str]) -> ToolResult:
        """Run a git command and return the result."""
        try:
            result = subprocess.run(
                command,
                cwd=self.repository.absolute_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return ToolResult(
                success=True,
                message="Command executed successfully",
                output=result.stdout.strip(),
            )
        except subprocess.CalledProcessError as e:
            return ToolResult(
                success=False,
                message=f"Command failed with exit code {e.returncode}",
                error=e.stderr.strip() if e.stderr else str(e),
            )
        except (OSError, FileNotFoundError) as e:
            return ToolResult(
                success=False, message="Command execution failed", error=str(e)
            )

    def git_status(self) -> ToolResult:
        """Get git status."""
        return self.run_git_command(["git", "status", "--porcelain"])

    def git_log(self, max_count: int = 10) -> ToolResult:
        """Get git log."""
        return self.run_git_command(
            ["git", "log", f"--max-count={max_count}", "--oneline", "--graph"]
        )

    def git_branches(self) -> ToolResult:
        """List all branches."""
        return self.run_git_command(["git", "branch", "-a"])

    def git_remotes(self) -> ToolResult:
        """List remote repositories."""
        return self.run_git_command(["git", "remote", "-v"])

    def git_diff(self, staged: bool = False) -> ToolResult:
        """Show git diff."""
        command = ["git", "diff"]
        if staged:
            command.append("--staged")
        return self.run_git_command(command)

    def git_clean_dry_run(self) -> ToolResult:
        """Show what would be cleaned (dry run)."""
        return self.run_git_command(["git", "clean", "-n", "-d"])

    def git_gc(self) -> ToolResult:
        """Run git garbage collection."""
        return self.run_git_command(["git", "gc", "--auto"])
