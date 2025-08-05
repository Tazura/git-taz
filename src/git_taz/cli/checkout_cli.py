"""CLI implementation for checkout functionality."""

import sys
from typing import Optional
from ..models import GitRepository
from ..services import GitOperationsService


class CheckoutCLI:
    """Command-line interface for checkout operations."""

    def __init__(self, repo_path: Optional[str] = None):
        try:
            self.repository = GitRepository.from_path(repo_path or ".")
            self.git_operations = GitOperationsService(self.repository)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    def list_branches(self) -> None:
        """List all branches."""
        branches = self.git_operations.get_branches()
        current = self.git_operations.get_current_branch()

        print("Branches:")
        for branch in branches:
            marker = "* " if branch == current else "  "
            print(f"{marker}{branch}")

    def list_tags(self) -> None:
        """List all tags."""
        tags = self.git_operations.get_tags()

        print("Tags:")
        for tag in tags:
            print(f"  {tag}")

    def checkout_interactive(self) -> None:
        """Interactive checkout selection."""
        print("Select checkout target type:")
        print("1. Branches")
        print("2. Tags")

        try:
            choice = input("Enter choice (1-2): ").strip()
        except KeyboardInterrupt:
            print("\nCancelled.")
            return

        if choice == "1":
            self._checkout_from_list("branches")
        elif choice == "2":
            self._checkout_from_list("tags")
        else:
            print("Invalid choice.")

    def _checkout_from_list(self, target_type: str) -> None:
        """Show list and checkout selected target."""
        if target_type == "branches":
            targets = self.git_operations.get_branches()
            print("\nAvailable branches:")
        else:
            targets = self.git_operations.get_tags()
            print("\nAvailable tags:")

        if not targets:
            print(f"No {target_type} found.")
            return

        for i, target in enumerate(targets, 1):
            print(f"{i}. {target}")

        try:
            choice = input(
                f"\nEnter number (1-{len(targets)}) or 'q' to quit: "
            ).strip()
        except KeyboardInterrupt:
            print("\nCancelled.")
            return

        if choice.lower() == "q":
            return

        try:
            index = int(choice) - 1
            if 0 <= index < len(targets):
                target = targets[index]
                result = self.git_operations.checkout(target)
                print(result.message)
                if not result.success:
                    sys.exit(1)
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input.")

    def checkout_direct(self, target: str) -> None:
        """Checkout a specific branch or tag directly."""
        result = self.git_operations.checkout(target)
        print(result.message)
        if not result.success:
            sys.exit(1)
