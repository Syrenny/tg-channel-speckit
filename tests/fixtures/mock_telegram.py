"""Mock Telegram client for testing."""
from datetime import datetime, timezone
from typing import AsyncIterator, Optional
from unittest.mock import MagicMock, AsyncMock


class MockUser:
    """Mock Telegram user."""

    def __init__(
        self,
        id: int,
        username: Optional[str] = None,
        first_name: str = 'Test',
        last_name: Optional[str] = None
    ):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name


class MockMessage:
    """Mock Telegram message (post or comment)."""

    def __init__(
        self,
        id: int,
        text: str = '',
        date: Optional[datetime] = None,
        views: Optional[int] = None,
        sender: Optional[MockUser] = None,
        reply_to: Optional[int] = None
    ):
        self.id = id
        self.text = text
        self.date = date or datetime.now(timezone.utc)
        self.views = views
        self.sender = sender
        self.reply_to = MagicMock()
        self.reply_to.reply_to_msg_id = reply_to


class MockChannel:
    """Mock Telegram channel."""

    def __init__(
        self,
        id: int,
        username: Optional[str] = None,
        title: str = 'Test Channel'
    ):
        self.id = id
        self.username = username
        self.title = title


def create_mock_telegram_client(
    channel: Optional[MockChannel] = None,
    posts: Optional[list[MockMessage]] = None,
    comments: Optional[dict[int, list[MockMessage]]] = None
):
    """
    Create a mock TelegramClient for testing.

    Args:
        channel: Mock channel to return
        posts: List of mock posts
        comments: Dict mapping post_id to list of comments

    Returns:
        Mock TelegramClient
    """
    client = AsyncMock()

    # Default mocks
    if channel is None:
        channel = MockChannel(id=123456789, username='test_channel', title='Test Channel')
    if posts is None:
        posts = []
    if comments is None:
        comments = {}

    # Mock get_entity
    client.get_entity = AsyncMock(return_value=channel)

    # Mock iter_messages for posts
    async def mock_iter_messages(entity, limit=None, reply_to=None):
        if reply_to is not None:
            # Return comments for specific post
            for comment in comments.get(reply_to, []):
                yield comment
        else:
            # Return posts
            for post in posts[:limit] if limit else posts:
                yield post

    client.iter_messages = mock_iter_messages

    # Mock connect/disconnect
    client.connect = AsyncMock()
    client.disconnect = AsyncMock()
    client.is_connected = MagicMock(return_value=True)

    # Mock start (authorization)
    client.start = AsyncMock()

    return client


def create_sample_data():
    """
    Create sample test data for a channel.

    Returns:
        Tuple of (channel, posts, comments)
    """
    channel = MockChannel(
        id=123456789,
        username='sample_channel',
        title='Sample Channel'
    )

    user1 = MockUser(id=1001, username='user1', first_name='Alice', last_name='Smith')
    user2 = MockUser(id=1002, username='user2', first_name='Bob', last_name=None)

    posts = [
        MockMessage(id=1, text='First post', views=100, date=datetime(2026, 2, 1, 10, 0, 0, tzinfo=timezone.utc)),
        MockMessage(id=2, text='Second post', views=200, date=datetime(2026, 2, 2, 10, 0, 0, tzinfo=timezone.utc)),
    ]

    comments = {
        1: [
            MockMessage(id=101, text='Great!', sender=user1, reply_to=1),
            MockMessage(id=102, text='Thanks', sender=user2, reply_to=1),
        ],
        2: [
            MockMessage(id=201, text='Interesting', sender=user1, reply_to=2),
        ],
    }

    return channel, posts, comments
