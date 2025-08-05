"""Git tools and utilities."""

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
            "diff": GitTool(
                name="Git Diff",
                description="Show changes between commits",
                category="Analysis",
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

    def git_status(self) -> "ToolResult":
        """Get git status using GitPython."""
        try:
            if not self.repository.repo:
                return ToolResult(success=False, message="No repository loaded")

            # Get status information
            repo = self.repository.repo
            status_info = []

            # Untracked files
            untracked = repo.untracked_files
            for file in untracked:
                status_info.append(f"?? {file}")

            # Modified files
            for item in repo.index.diff(None):
                status_info.append(f" M {item.a_path}")

            # Staged files
            for item in repo.index.diff("HEAD"):
                status_info.append(f"M  {item.a_path}")

            output = "\n".join(status_info) if status_info else "No changes"
            return ToolResult(success=True, message="Status retrieved", output=output)
        except Exception as e:
            return ToolResult(success=False, message=f"Error getting status: {e}")

    def git_log(self, max_count: int = 15) -> "ToolResult":
        """Get git log using GitPython."""
        try:
            if not self.repository.repo:
                return ToolResult(success=False, message="No repository loaded")

            repo = self.repository.repo
            commits = list(repo.iter_commits(max_count=max_count))

            log_lines = []
            for commit in commits:
                # Format similar to your git log format
                date_str = commit.committed_datetime.strftime("%Y-%m-%d %H:%M")
                author = (commit.author.name or "Unknown")[:22]
                short_hash = str(commit.hexsha)[:7]
                message = str(commit.message).strip().split("\n")[0][:80]

                log_line = f"{date_str} {author:<22} {short_hash} {message}"
                log_lines.append(log_line)

            output = "\n".join(log_lines)
            return ToolResult(success=True, message="Log retrieved", output=output)
        except Exception as e:
            return ToolResult(success=False, message=f"Error getting log: {e}")

    def git_branches(self) -> "ToolResult":
        """Get git branches using GitPython."""

        try:
            if not self.repository.repo:
                return ToolResult(success=False, message="No repository loaded")

            repo = self.repository.repo
            branches = []

            # Local branches
            for branch in repo.branches:
                marker = "* " if branch == repo.active_branch else "  "
                branches.append(f"{marker}{branch.name}")

            # Remote branches
            for remote in repo.remotes:
                for ref in remote.refs:
                    branches.append(f"  remotes/{ref.name}")

            output = "\n".join(branches)
            return ToolResult(success=True, message="Branches retrieved", output=output)
        except Exception as e:
            return ToolResult(success=False, message=f"Error getting branches: {e}")

    def git_diff(self, staged: bool = False) -> "ToolResult":
        """Get git diff using GitPython."""

        try:
            if not self.repository.repo:
                return ToolResult(success=False, message="No repository loaded")

            repo = self.repository.repo

            if staged:
                diff = repo.index.diff("HEAD")
            else:
                diff = repo.index.diff(None)

            diff_lines = []
            for item in diff:
                diff_lines.append(f"diff --git a/{item.a_path} b/{item.b_path}")
                if item.change_type == "M":
                    diff_lines.append(f"Modified: {item.a_path}")
                elif item.change_type == "A":
                    diff_lines.append(f"Added: {item.a_path}")
                elif item.change_type == "D":
                    diff_lines.append(f"Deleted: {item.a_path}")

            output = "\n".join(diff_lines) if diff_lines else "No differences"
            return ToolResult(success=True, message="Diff retrieved", output=output)
        except Exception as e:
            return ToolResult(success=False, message=f"Error getting diff: {e}")
