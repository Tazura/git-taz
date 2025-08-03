# Contributing to Git-Taz

Thank you for your interest in contributing to Git-Taz! This document provides guidelines and information for contributors.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Tazura/git-taz.git
   cd git-taz
   ```

2. **Install uv** (recommended package manager)
   ```bash
   # On macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Install dependencies**
   ```bash
   uv sync --extra dev
   ```

4. **Install pre-commit hooks** (optional but recommended)
   ```bash
   uv run pre-commit install
   ```

## Code Style and Quality

We use several tools to maintain code quality:

- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking
- **Pytest** for testing

### Running Quality Checks

```bash
# Format code
uv run black .

# Lint code
uv run flake8 .

# Type checking
uv run mypy .

# Run tests
uv run pytest

# Run all checks
uv run pre-commit run --all-files
```

## Testing

- Write tests for new functionality in the `tests/` directory
- Follow the existing test patterns and naming conventions
- Ensure all tests pass before submitting a PR
- Aim for good test coverage

```bash
# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing
```

## UI Development

The application uses `npyscreen` for the terminal user interface:

- Forms are in separate files under `src/git_taz/ui/`
- Follow the existing patterns for keyboard shortcuts and navigation
- Test UI changes manually as automated UI testing is limited
- Document any new keyboard shortcuts in help text and README

## Submitting Changes

1. **Fork the repository** and create a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines

3. **Add tests** for new functionality

4. **Run the quality checks** to ensure everything passes

5. **Commit your changes** with clear, descriptive messages
   ```bash
   git commit -m "Add feature: description of what you added"
   ```

6. **Push to your fork** and create a pull request
   ```bash
   git push origin feature/your-feature-name
   ```

## Pull Request Guidelines

- **Use the PR template** when creating a pull request
- **Write clear descriptions** of what changes you made and why
- **Link related issues** if applicable
- **Ensure CI passes** before requesting review
- **Respond to feedback** promptly and professionally

## Code Review Process

1. All PRs require at least one review
2. CI must pass (tests, linting, type checking)
3. Changes should be well-documented
4. Breaking changes require special consideration

## Reporting Issues

- Use the issue templates for bug reports and feature requests
- Include relevant information (OS, Python version, etc.)
- Provide clear reproduction steps for bugs
- Search existing issues before creating new ones

## Questions?

Feel free to open an issue for questions about contributing or reach out to the maintainers.

Thank you for contributing to Git-Taz! 🎉
