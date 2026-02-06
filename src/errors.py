"""Custom error classes for the channel loader."""


class LoaderError(Exception):
    """Base class for loader errors."""
    pass


class AuthError(LoaderError):
    """Raised when Telegram authentication fails."""

    def __init__(self, message: str = "Authentication failed"):
        self.message = message
        self.suggestion = "Check your TELEGRAM_API_ID and TELEGRAM_API_HASH in .env file"
        super().__init__(self.message)


class AccessError(LoaderError):
    """Raised when access to a channel is denied."""

    def __init__(self, channel: str, message: str = "Access denied"):
        self.channel = channel
        self.message = message
        self.suggestion = f"Make sure you have access to the channel '{channel}'"
        super().__init__(self.message)


class NetworkError(LoaderError):
    """Raised when a network error occurs."""

    def __init__(self, message: str = "Network error"):
        self.message = message
        self.suggestion = "Check your internet connection and try again"
        super().__init__(self.message)
