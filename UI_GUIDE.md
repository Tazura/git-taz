# Git-Taz UI Guide

## New Textual-based Interface

Git-Taz now features a modern, responsive terminal UI built with Textual and Rich libraries, replacing the previous npyscreen implementation.

## Interface Layout

```
┌─ Header: Git-Taz - Git Utility Tool ─────────────────────────────┐
│ ┌─ Sidebar (30%) ─┐ ┌─ Main Area (70%) ───────────────────────┐ │
│ │ Repository       │ │ ┌─ Repository Information ───────────┐ │ │
│ │ Browser         │ │ │ Path: /path/to/repo                │ │ │
│ │                 │ │ │ Name: repo-name                    │ │ │
│ │ [Directory Tree]│ │ │ Git Repo: Yes                      │ │ │
│ │                 │ │ │ Exists: Yes                        │ │ │
│ │                 │ │ └────────────────────────────────────┘ │ │
│ │                 │ │ ┌─ Git Tools ────────────────────────┐ │ │
│ │                 │ │ │ [Status] [Log] [Diff]              │ │ │
│ │                 │ │ │ [Branches] [Remotes]               │ │ │
│ │                 │ │ └────────────────────────────────────┘ │ │
│ │                 │ │ ┌─ Output ───────────────────────────┐ │ │
│ │                 │ │ │ Command output appears here...     │ │ │
│ │                 │ │ │ [Colored log messages]             │ │ │
│ │                 │ │ └────────────────────────────────────┘ │ │
│ └─────────────────┘ └─────────────────────────────────────────┘ │
└─ Footer: Key bindings ───────────────────────────────────────────┘
```

## Key Bindings

- **Ctrl+Q / Ctrl+C**: Quit the application
- **Ctrl+R**: Refresh repository information
- **Ctrl+T**: Toggle sidebar visibility
- **Tab**: Navigate between widgets
- **Enter**: Activate buttons/select items

## Git Tools

### Available Tools
- **Status**: Show working tree status (`git status`)
- **Log**: Display commit history (`git log`)
- **Diff**: Show changes between commits (`git diff`)
- **Branches**: List all branches (`git branch -a`)
- **Remotes**: Show remote repositories (`git remote -v`)

### Output Colors
- 🟢 **Green**: Successful operations
- 🔴 **Red**: Errors and failures
- 🟡 **Yellow**: Warnings
- ⚪ **White**: General information

## Features

### Repository Browser
- Navigate through repository files and directories
- Click on files to view selection in output log
- Automatically loads the specified repository on startup

### Repository Information Panel
- Shows repository path, name, and status
- Indicates if the directory is a valid Git repository
- Updates when refreshing (Ctrl+R)

### Interactive Git Operations
- Click buttons to execute Git commands
- Real-time feedback in the output log
- Proper error handling and reporting

### Responsive Design
- Toggle sidebar with Ctrl+T for more output space
- CSS-based styling for consistent appearance
- Adaptive layout for different terminal sizes

## Usage Examples

### Basic Usage
```bash
# Run with current directory
git-taz

# Run with specific repository
git-taz --repo /path/to/repo
git-taz -r ./my-project
```

### Testing with Sample Repository
```bash
# Create a sample repository for testing
python scripts/create_sample_repo.py

# Run git-taz with the sample repo
git-taz --repo test-repo
```

## Development

The new UI is built with:
- **Textual**: Modern Python TUI framework
- **Rich**: Library for rich text and beautiful formatting
- **Async/Await**: Proper asynchronous operation handling
- **Type Safety**: Full mypy compliance

### Key Files
- `src/git_taz/ui/app.py`: Main Textual application
- `src/git_taz/ui/__init__.py`: UI module entry point
- `src/git_taz/core.py`: Application core and argument parsing

## Migration from npyscreen

The application has been completely migrated from npyscreen to Textual:
- ✅ Modern, responsive terminal interface
- ✅ Better keyboard navigation
- ✅ Rich text formatting and colors
- ✅ Async operation support
- ✅ Type-safe implementation
- ✅ CSS-like styling capabilities
