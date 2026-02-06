"""Unit tests for configuration loading."""
import os
import pytest
from unittest.mock import patch


class TestConfigLoader:
    """Tests for config.py module."""

    def test_load_config_success(self):
        """Config loads successfully with valid .env."""
        from src.config import load_config

        with patch.dict(os.environ, {
            'TELEGRAM_API_ID': '12345',
            'TELEGRAM_API_HASH': 'abc123hash'
        }):
            config = load_config()
            assert config['api_id'] == 12345
            assert config['api_hash'] == 'abc123hash'

    def test_load_config_missing_api_id(self):
        """Config raises error when API_ID is missing."""
        from src.config import load_config, ConfigError

        with patch.dict(os.environ, {'TELEGRAM_API_HASH': 'abc123'}, clear=True):
            with pytest.raises(ConfigError) as exc_info:
                load_config()
            assert 'TELEGRAM_API_ID' in str(exc_info.value)

    def test_load_config_missing_api_hash(self):
        """Config raises error when API_HASH is missing."""
        from src.config import load_config, ConfigError

        with patch.dict(os.environ, {'TELEGRAM_API_ID': '12345'}, clear=True):
            with pytest.raises(ConfigError) as exc_info:
                load_config()
            assert 'TELEGRAM_API_HASH' in str(exc_info.value)

    def test_load_config_invalid_api_id(self):
        """Config raises error when API_ID is not numeric."""
        from src.config import load_config, ConfigError

        with patch.dict(os.environ, {
            'TELEGRAM_API_ID': 'not_a_number',
            'TELEGRAM_API_HASH': 'abc123'
        }):
            with pytest.raises(ConfigError) as exc_info:
                load_config()
            assert 'numeric' in str(exc_info.value).lower() or 'invalid' in str(exc_info.value).lower()
