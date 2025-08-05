"""Main module for git-taz functionality."""

import argparse


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
  %(prog)s                              Launch interactive UI mode (default)
  %(prog)s --repo /path/to/repo         Launch UI with specific repository
  %(prog)s -r .                         Launch UI for current directory

  %(prog)s checkout --interactive       Interactive branch/tag checkout
  %(prog)s checkout main                Checkout 'main' branch directly
  %(prog)s checkout --list-branches     List all branches
  %(prog)s checkout --list-tags         List all tags
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

    # Add subcommands for CLI operations
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Checkout subcommand
    checkout_parser = subparsers.add_parser(
        "checkout", help="Checkout branches/tags via CLI"
    )
    checkout_parser.add_argument("target", nargs="?", help="Branch or tag to checkout")
    checkout_parser.add_argument(
        "--interactive", "-i", action="store_true", help="Interactive selection mode"
    )
    checkout_parser.add_argument(
        "--list-branches", action="store_true", help="List all branches"
    )
    checkout_parser.add_argument(
        "--list-tags", action="store_true", help="List all tags"
    )

    return parser.parse_args()


def main() -> None:
    """Main entry point for the application."""
    args = parse_arguments()

    # Handle CLI commands
    if args.command == "checkout":
        from .cli import CheckoutCLI

        repo_path = args.repo if args.repo != "." else None
        cli = CheckoutCLI(repo_path)

        if args.list_branches:
            cli.list_branches()
        elif args.list_tags:
            cli.list_tags()
        elif args.interactive or not args.target:
            cli.checkout_interactive()
        else:
            cli.checkout_direct(args.target)
        return

    # Default behavior is to launch UI mode
    # Pass repository path to UI if specified
    repo_path = args.repo if args.repo != "." else None

    from .ui import run_ui

    run_ui(repo_path)
    return


if __name__ == "__main__":
    main()
