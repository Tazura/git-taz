"""Main module for git-taz functionality."""

import argparse
from pathlib import Path


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

    # Future: Add command subparsers here for specific git operations
    # parser.add_subparsers(dest='command', help='Available commands')

    return parser.parse_args()


def main() -> None:
    """Main entry point for the application."""
    args = parse_arguments()

    # Default behavior is to launch UI mode
    # Only run command-line mode if --no-ui is specified or commands are given
    from .ui import run_ui

    run_ui()
    return


if __name__ == "__main__":
    main()
