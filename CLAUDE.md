# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Setup and Dependencies
```bash
# Install dependencies with dev extras
uv sync --extra dev

# Install pre-commit hooks (recommended)
uv run pre-commit install
```

### Testing and Quality Checks
```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run single test file
uv run pytest tests/test_core.py

# Code formatting
uv run black .

# Linting
uv run flake8 .

# Type checking
uv run mypy .

# Run all quality checks
uv run pre-commit run --all-files
```

### Running the Application
```bash
# Launch interactive UI (default)
git-taz

# Launch with specific repository
git-taz --repo /path/to/repo

# Launch for current directory
git-taz -r .
```

## Architecture Overview

Git-Taz is a terminal-based Git utility tool built with Python, using the Textual framework for the UI and GitPython for Git operations.

### Core Components

- **Entry Point**: `src/git_taz/core.py` - Main entry point with argument parsing and UI launcher
- **UI Layer**: `src/git_taz/ui/app.py` - Textual-based terminal UI with Rich formatting
- **Data Models**: `src/git_taz/models/__init__.py` - GitRepository, GitTool, and ToolResult models
- **Tools Layer**: `src/git_taz/tools/__init__.py` - GitToolsManager for Git operations using GitPython

### UI Architecture (Textual Framework)

The application uses a horizontal layout with:
- **Sidebar** (25%): Repository info, file tree navigation
- **Main Panel** (75%): 
  - Tools menu (Git operations like status, log, branches, diff)
  - Commit history table (DataTable widget)
  - Command output log (Log widget)

Key UI bindings:
- `ctrl+c/ctrl+q`: Quit
- `ctrl+r`: Refresh repository
- `ctrl+t`: Toggle sidebar

### Git Operations

All Git operations are handled through GitPython (not shell commands) for better integration and error handling. The GitToolsManager provides methods for:
- `git_status()`: Working tree status
- `git_log()`: Commit history 
- `git_branches()`: Local and remote branches
- `git_diff()`: File differences

### Type Checking Configuration

MyPy is configured with strict settings but relaxed for UI components due to Textual's complex typing. The configuration in `mypy.ini` excludes UI modules from strict type checking while maintaining high standards for core logic.

### Development Notes

- Uses Python 3.13+ with modern dependency management via `uv`
- UI components are tested manually as Textual automated testing is limited
- Pre-commit hooks enforce code quality (Black, Flake8, MyPy, Bandit)
- Security scanning with Bandit and Safety tools
- CSS-like styling for Textual widgets with themes and responsive layout