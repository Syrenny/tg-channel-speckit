"""Telegram client wrapper using Telethon."""
import asyncio
from datetime import timezone
from pathlib import Path
from typing import AsyncIterator, Optional

from telethon import TelegramClient as TelethonClient
from telethon.errors import (
    AuthKeyUnregisteredError,
    ChannelPrivateError,
    FloodWaitError,
    RPCError,
)
from telethon.tl.types import Channel as TelethonChannel, User

from src.config import load_config
from src.errors import AuthError, AccessError, NetworkError
from src.models import Author, Channel, Comment, Post


# Session file location
SESSION_DIR = Path('.specify-for-tg-analysis/tg')
SESSION_NAME = 'session'


class TelegramClientWrapper:
    """Wrapper around Telethon client for channel data extraction."""

    def __init__(self, api_id: int, api_hash: str):
        """
        Initialize the Telegram client.

        Args:
            api_id: Telegram API ID
            api_hash: Telegram API hash
        """
        # Ensure session directory exists
        SESSION_DIR.mkdir(parents=True, exist_ok=True)
        session_path = SESSION_DIR / SESSION_NAME

        self._client = TelethonClient(
            str(session_path),
            api_id,
            api_hash
        )
        self._client.flood_sleep_threshold = 60  # Auto-wait up to 60 seconds

    async def connect(self) -> None:
        """Connect to Telegram and authorize if needed."""
        try:
            await self._client.connect()
            if not await self._client.is_user_authorized():
                # Start interactive authorization
                await self._client.start()
        except AuthKeyUnregisteredError:
            raise AuthError("Session expired. Please re-authenticate.")
        except Exception as e:
            raise NetworkError(f"Failed to connect: {e}")

    async def disconnect(self) -> None:
        """Disconnect from Telegram."""
        await self._client.disconnect()

    async def get_channel_info(self, channel_id: str) -> Channel:
        """
        Get channel information.

        Args:
            channel_id: Channel username (with or without @) or URL

        Returns:
            Channel object with basic info

        Raises:
            AccessError: If channel is private or doesn't exist
        """
        # Normalize channel ID
        channel_id = channel_id.replace('https://t.me/', '').lstrip('@')

        try:
            entity = await self._client.get_entity(channel_id)

            if isinstance(entity, TelethonChannel):
                return Channel(
                    id=entity.id,
                    username=entity.username,
                    title=entity.title,
                    posts=[]
                )
            else:
                raise AccessError(channel_id, "Not a channel")

        except ChannelPrivateError:
            raise AccessError(channel_id, "Channel is private")
        except ValueError as e:
            raise AccessError(channel_id, f"Channel not found: {e}")

    async def get_posts(
        self,
        channel: Channel,
        limit: Optional[int] = None
    ) -> AsyncIterator[Post]:
        """
        Get posts from a channel.

        Args:
            channel: Channel to get posts from
            limit: Maximum number of posts to retrieve

        Yields:
            Post objects
        """
        try:
            async for message in self._client.iter_messages(
                channel.id,
                limit=limit
            ):
                # Skip non-text messages or service messages
                if message.text is None:
                    text = ''
                else:
                    text = message.text

                yield Post(
                    id=message.id,
                    text=text,
                    date=message.date.replace(tzinfo=timezone.utc) if message.date else None,
                    views=message.views,
                    comments=[]
                )

        except FloodWaitError as e:
            # This should be handled automatically by flood_sleep_threshold
            # but we catch it just in case
            await asyncio.sleep(e.seconds)
            # Retry by calling ourselves again (simplified)
            async for post in self.get_posts(channel, limit):
                yield post

    async def get_comments(
        self,
        channel: Channel,
        post_id: int
    ) -> AsyncIterator[Comment]:
        """
        Get comments for a specific post.

        Args:
            channel: Channel containing the post
            post_id: ID of the post to get comments for

        Yields:
            Comment objects with author information
        """
        try:
            async for message in self._client.iter_messages(
                channel.id,
                reply_to=post_id
            ):
                # Extract author info
                sender = message.sender
                if isinstance(sender, User):
                    author = Author(
                        user_id=sender.id,
                        username=sender.username,
                        first_name=sender.first_name or '',
                        last_name=sender.last_name
                    )
                else:
                    # Anonymous or channel post
                    author = Author(
                        user_id=0,
                        username=None,
                        first_name='Anonymous',
                        last_name=None
                    )

                yield Comment(
                    id=message.id,
                    text=message.text or '',
                    date=message.date.replace(tzinfo=timezone.utc) if message.date else None,
                    author=author
                )

        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
            async for comment in self.get_comments(channel, post_id):
                yield comment


def create_client() -> TelegramClientWrapper:
    """
    Create a TelegramClientWrapper with config from .env.

    Returns:
        Configured TelegramClientWrapper instance
    """
    config = load_config()
    return TelegramClientWrapper(config['api_id'], config['api_hash'])
