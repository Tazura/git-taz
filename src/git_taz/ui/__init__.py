"""UI components for git-taz application."""

import locale
import os
from typing import Optional

# Fix locale issues before importing npyscreen
os.environ.setdefault("LANG", "C.UTF-8")
os.environ.setdefault("LC_ALL", "C.UTF-8")

# Patch locale.setlocale to handle errors gracefully
_original_setlocale = locale.setlocale


def _patched_setlocale(category: int, locale_name: Optional[str] = None) -> str:
    """Patched setlocale that falls back to C locale on errors."""
    try:
        if locale_name == "":
            # Try common fallbacks for empty locale string
            for fallback in ["C.UTF-8", "en_US.UTF-8", "C"]:
                try:
                    return _original_setlocale(category, fallback)
                except locale.Error:
                    continue
            # If all fallbacks fail, use C
            return _original_setlocale(category, "C")
        else:
            return _original_setlocale(category, locale_name)
    except locale.Error:
        # Final fallback to C locale
        return _original_setlocale(category, "C")


# Apply the patch
locale.setlocale = _patched_setlocale

from .app import GitTazApp  # noqa: E402


def run_ui() -> None:
    """Run the npyscreen UI."""
    # Fix locale issues that can occur in some environments
    try:
        locale.setlocale(locale.LC_ALL, "")
    except locale.Error:
        # Fallback to C locale if system locale is not available
        try:
            locale.setlocale(locale.LC_ALL, "C.UTF-8")
        except locale.Error:
            locale.setlocale(locale.LC_ALL, "C")

    # Set environment variable to prevent ncurses locale issues
    os.environ.setdefault("LANG", "en_US.UTF-8")

    try:
        app = GitTazApp()
        app.run()
    except KeyboardInterrupt:
        pass  # Clean exit on Ctrl+C
