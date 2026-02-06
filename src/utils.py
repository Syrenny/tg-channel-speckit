"""Utility functions for the channel loader."""
import json
import os
import sys
from pathlib import Path
from typing import Optional


def ensure_dir(path: str) -> None:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure exists
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def format_error(error_type: str, message: str, suggestion: Optional[str] = None) -> str:
    """
    Format an error message for display.

    Args:
        error_type: Type of error (e.g., 'AuthError')
        message: Error message
        suggestion: Optional suggestion for fixing the error

    Returns:
        Formatted error string
    """
    result = f"Error [{error_type}]: {message}"
    if suggestion:
        result += f"\nSuggestion: {suggestion}"
    return result


def save_to_json(data: dict, path: str) -> None:
    """
    Save data to a JSON file.

    Args:
        data: Dictionary to save
        path: File path to save to
    """
    # Ensure parent directory exists
    ensure_dir(os.path.dirname(path))

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def print_progress(message: str, end: str = '\n') -> None:
    """
    Print a progress message to stdout.

    Args:
        message: Message to print
        end: Line ending (default: newline)
    """
    print(message, end=end, flush=True)


def print_error(message: str) -> None:
    """
    Print an error message to stderr.

    Args:
        message: Error message to print
    """
    print(message, file=sys.stderr)
