"""Unit tests for utility functions."""
import os
import tempfile
import pytest


class TestEnsureDir:
    """Tests for ensure_dir function."""

    def test_ensure_dir_creates_directory(self):
        """ensure_dir creates directory if it doesn't exist."""
        from src.utils import ensure_dir

        with tempfile.TemporaryDirectory() as tmpdir:
            new_dir = os.path.join(tmpdir, 'new', 'nested', 'dir')
            ensure_dir(new_dir)
            assert os.path.isdir(new_dir)

    def test_ensure_dir_existing_directory(self):
        """ensure_dir does nothing if directory exists."""
        from src.utils import ensure_dir

        with tempfile.TemporaryDirectory() as tmpdir:
            ensure_dir(tmpdir)  # Should not raise
            assert os.path.isdir(tmpdir)


class TestFormatError:
    """Tests for format_error function."""

    def test_format_error_basic(self):
        """format_error returns formatted error message."""
        from src.utils import format_error

        result = format_error('AuthError', 'Invalid credentials')
        assert 'AuthError' in result
        assert 'Invalid credentials' in result

    def test_format_error_with_suggestion(self):
        """format_error includes suggestion when provided."""
        from src.utils import format_error

        result = format_error('ConfigError', 'Missing API_ID', 'Check your .env file')
        assert 'ConfigError' in result
        assert 'Missing API_ID' in result
        assert 'Check your .env file' in result
