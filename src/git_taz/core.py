"""Main module for git-taz functionality."""


def greet(name: str = "git-taz") -> str:
    """Return a greeting message.

    Args:
        name: The name to greet.

    Returns:
        A greeting message.
    """
    return f"Hello from {name}!"


def main() -> None:
    """Main entry point for the application."""
    message = greet()
    print(message)


if __name__ == "__main__":
    main()
