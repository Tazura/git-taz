# Git-Taz

[![CI](https://github.com/Tazura/git-taz/actions/workflows/ci.yml/badge.svg)](https://github.com/Tazura/git-taz/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Tazura/git-taz/branch/main/graph/badge.svg)](https://codecov.io/gh/Tazura/git-taz)

A Git utility tool with an interactive terminal user interface.

## Features

- Interactive terminal UI using npyscreen
- Repository selection and validation
- Git tool selection and execution
- Command-driven interface with keyboard shortcuts
- Support for multiple git operations

## Installation

```bash
# Install with uv (recommended)
uv add git-taz

# Or with pip
pip install git-taz
```

## Usage

```bash
# Launch interactive UI (default)
git-taz

# Launch UI with specific repository
git-taz --repo /path/to/repo

# Launch UI for current directory
git-taz -r .
```

### Keyboard Shortcuts

- **F2**: Show command selection
- **CTRL-H**: Show help
- **CTRL-X / CTRL-C**: Exit application
- **ESC**: Cancel/Go back

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development setup and guidelines.

```bash
# Quick start
git clone https://github.com/Tazura/git-taz.git
cd git-taz
uv sync --extra dev
uv run pytest
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

[Add your license here]
