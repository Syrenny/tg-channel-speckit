"""Configuration loading from .env file."""
import os
from pathlib import Path
from dotenv import load_dotenv


class ConfigError(Exception):
    """Raised when configuration is invalid or missing."""
    pass


def load_config() -> dict:
    """
    Load configuration from environment variables.

    Looks for .env file in project root and loads it.

    Returns:
        dict with 'api_id' (int) and 'api_hash' (str)

    Raises:
        ConfigError: If required variables are missing or invalid
    """
    # Try to load .env from project root
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)

    # Get required variables
    api_id = os.environ.get('TELEGRAM_API_ID')
    api_hash = os.environ.get('TELEGRAM_API_HASH')

    # Validate API_ID
    if not api_id:
        raise ConfigError(
            "TELEGRAM_API_ID is not set. "
            "Please create a .env file with your Telegram API credentials. "
            "Get them from https://my.telegram.org"
        )

    try:
        api_id_int = int(api_id)
    except ValueError:
        raise ConfigError(
            f"TELEGRAM_API_ID must be numeric, got: {api_id}"
        )

    # Validate API_HASH
    if not api_hash:
        raise ConfigError(
            "TELEGRAM_API_HASH is not set. "
            "Please create a .env file with your Telegram API credentials. "
            "Get them from https://my.telegram.org"
        )

    return {
        'api_id': api_id_int,
        'api_hash': api_hash,
    }
