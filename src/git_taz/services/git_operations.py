"""Git operations service for git-taz."""

from typing import List, Tuple, Optional
from ..models import GitRepository
from ..tools import GitToolsManager


class CheckoutResult:
    """Result of a checkout operation."""

    def __init__(self, success: bool, message: str, target: Optional[str] = None):
        self.success = success
        self.message = message
        self.target = target


class GitOperationsService:
    """Service class for Git operations that can be used by both UI and CLI."""

    def __init__(self, repository: GitRepository):
        self.repository = repository
        self.tools_manager = GitToolsManager(repository)

    def get_branches(self) -> List[str]:
        """Get list of all branches."""
        if not self.repository.repo:
            return []
        return sorted(b.name for b in self.repository.repo.branches)

    def get_tags(self) -> List[str]:
        """Get list of all tags."""
        if not self.repository.repo:
            return []
        return sorted(t.name for t in self.repository.repo.tags)

    def get_checkout_targets(self, target_type: str) -> List[Tuple[str, str]]:
        """Get checkout targets formatted for UI Select widgets."""
        if target_type == "branches":
            names = self.get_branches()
        else:
            names = self.get_tags()

        return [(name, name) for name in names]

    def checkout(self, target: str) -> CheckoutResult:
        """Checkout a branch or tag."""
        if not self.repository.repo:
            return CheckoutResult(False, "No repository loaded")

        try:
            self.repository.repo.git.checkout(target)
            return CheckoutResult(True, f"Successfully checked out {target}", target)
        except Exception as e:
            return CheckoutResult(False, f"Checkout failed: {e}")

    def get_current_branch(self) -> Optional[str]:
        """Get the current branch name."""
        if not self.repository.repo:
            return None

        try:
            return self.repository.repo.active_branch.name
        except Exception:
            return None

    def get_status(self):
        """Get git status."""
        return self.tools_manager.git_status()

    def get_log(self):
        """Get git log."""
        return self.tools_manager.git_log()

    def get_branches_info(self):
        """Get branches info."""
        return self.tools_manager.git_branches()

    def get_diff(self):
        """Get git diff."""
        return self.tools_manager.git_diff()
