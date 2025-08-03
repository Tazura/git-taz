"""Main module for git-taz functionality."""

import argparse
from pathlib import Path


def greet(name: str = "git-taz") -> str:
    """Return a greeting message.

    Args:
        name: The name to greet.

    Returns:
        A greeting message.
    """
    return f"Hello from {name}!"


def validate_git_repository(repo_path: str) -> bool:
    """Validate if the given path is a git repository.

    Args:
        repo_path: Path to the repository to validate.

    Returns:
        True if the path is a valid git repository, False otherwise.
    """
    repo = Path(repo_path)
    if not repo.exists():
        return False
    if not repo.is_dir():
        return False
    git_dir = repo / ".git"
    return git_dir.exists()


def get_repository_info(repo_path: str) -> dict:
    """Get basic information about the git repository.

    Args:
        repo_path: Path to the repository.

    Returns:
        Dictionary containing repository information.
    """
    repo = Path(repo_path)
    repo_absolute = repo.absolute()

    # Handle current directory case where name might be empty
    repo_name = repo_absolute.name

    return {
        "path": str(repo_absolute),
        "name": repo_name,
        "exists": repo.exists(),
        "is_git": validate_git_repository(repo_path),
    }


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Git-taz: A Git utility tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                         Launch interactive UI mode (default)
  %(prog)s --repo /path/to/repo    Launch UI with specific repository
  %(prog)s -r .                    Launch UI for current directory
  %(prog)s --no-ui                 Disable UI mode (for future CLI commands)
        """,
    )

    parser.add_argument(
        "-r",
        "--repo",
        type=str,
        default=".",
        help="Path to the git repository (default: current directory)",
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    parser.add_argument(
        "--no-ui",
        action="store_true",
        help="Disable UI mode and run in command-line mode",
    )

    # Future: Add command subparsers here for specific git operations
    # parser.add_subparsers(dest='command', help='Available commands')

    return parser.parse_args()


def main() -> None:
    """Main entry point for the application."""
    args = parse_arguments()

    # Default behavior is to launch UI mode
    # Only run command-line mode if --no-ui is specified or commands are given
    if not args.no_ui:
        from .ui import run_ui

        run_ui()
        return

    # Command-line mode (currently minimal functionality)
    # Get repository path from arguments
    repo_path = args.repo

    # Validate and get repository information
    if not validate_git_repository(repo_path):
        print(f"Error: '{repo_path}' is not a valid git repository")
        return

    repo_info = get_repository_info(repo_path)

    # Display information
    if args.verbose:
        print(f"Processing repository: {repo_info['name']}")
        print(f"Repository path: {repo_info['path']}")
        print(f"Is git repository: {repo_info['is_git']}")
        print("-" * 50)

    # Main functionality
    message = greet(f"git-taz processing {repo_info['name']}")
    print(message)
    print("Note: Use without --no-ui flag to launch interactive mode")


if __name__ == "__main__":
    main()
