"""Integration tests for the channel loader."""
import json
import os
import tempfile
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from datetime import datetime, timezone

from src.models import Author, Comment, Post, Channel


class MockTelegramClientWrapper:
    """Mock TelegramClientWrapper for testing."""

    def __init__(self, channel: Channel, posts: list[Post]):
        self.channel = channel
        self.posts = posts

    async def connect(self):
        pass

    async def disconnect(self):
        pass

    async def get_channel_info(self, channel_id: str) -> Channel:
        return self.channel

    async def get_posts(self, channel: Channel, limit=None):
        for post in self.posts[:limit] if limit else self.posts:
            yield post

    async def get_comments(self, channel: Channel, post_id: int):
        for post in self.posts:
            if post.id == post_id:
                for comment in post.comments:
                    yield comment
                break


def create_sample_data():
    """Create sample test data."""
    author1 = Author(user_id=1001, username='user1', first_name='Alice', last_name='Smith')
    author2 = Author(user_id=1002, username='user2', first_name='Bob', last_name=None)

    comments1 = [
        Comment(id=101, text='Great!', date=datetime(2026, 2, 1, 10, 5, 0, tzinfo=timezone.utc), author=author1),
        Comment(id=102, text='Thanks', date=datetime(2026, 2, 1, 10, 10, 0, tzinfo=timezone.utc), author=author2),
    ]
    comments2 = [
        Comment(id=201, text='Interesting', date=datetime(2026, 2, 2, 10, 5, 0, tzinfo=timezone.utc), author=author1),
    ]

    posts = [
        Post(id=1, text='First post', date=datetime(2026, 2, 1, 10, 0, 0, tzinfo=timezone.utc), views=100, comments=comments1),
        Post(id=2, text='Second post', date=datetime(2026, 2, 2, 10, 0, 0, tzinfo=timezone.utc), views=200, comments=comments2),
    ]

    channel = Channel(id=123456789, username='sample_channel', title='Sample Channel', posts=[])

    return channel, posts


class TestChannelLoader:
    """Integration tests for loader.py."""

    @pytest.mark.asyncio
    async def test_load_channel_basic(self):
        """Load channel data creates valid JSON file."""
        from src.loader import load_channel

        channel, posts = create_sample_data()
        mock_client = MockTelegramClientWrapper(channel, posts)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'test_channel.json')

            result = await load_channel(
                client=mock_client,
                channel_id='@sample_channel',
                output_path=output_path
            )

            # Verify file was created
            assert os.path.exists(output_path)

            # Verify JSON structure
            with open(output_path, 'r') as f:
                data = json.load(f)

            assert data['version'] == '1.0'
            assert data['status'] == 'complete'
            assert 'channel' in data
            assert data['channel']['id'] == 123456789

    @pytest.mark.asyncio
    async def test_load_channel_with_comments(self):
        """Load channel data includes comments with authors."""
        from src.loader import load_channel

        channel, posts = create_sample_data()
        mock_client = MockTelegramClientWrapper(channel, posts)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'test_channel.json')

            await load_channel(
                client=mock_client,
                channel_id='@sample_channel',
                output_path=output_path
            )

            with open(output_path, 'r') as f:
                data = json.load(f)

            # Check posts exist
            assert len(data['channel']['posts']) == 2

            # Check comments on first post
            first_post = data['channel']['posts'][0]
            assert len(first_post['comments']) == 2

            # Check author info
            first_comment = first_post['comments'][0]
            assert 'author' in first_comment
            assert first_comment['author']['user_id'] == 1001

    @pytest.mark.asyncio
    async def test_load_channel_empty_comments(self):
        """Load channel handles posts without comments."""
        from src.loader import load_channel

        channel = Channel(id=1, username='empty', title='Empty', posts=[])
        posts = [Post(id=1, text='No comments', date=datetime.now(timezone.utc), views=10, comments=[])]

        mock_client = MockTelegramClientWrapper(channel, posts)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'empty.json')

            await load_channel(
                client=mock_client,
                channel_id='@empty',
                output_path=output_path
            )

            with open(output_path, 'r') as f:
                data = json.load(f)

            assert data['channel']['posts'][0]['comments'] == []

    @pytest.mark.asyncio
    async def test_load_channel_counts(self):
        """Load channel calculates correct counts."""
        from src.loader import load_channel

        channel, posts = create_sample_data()
        mock_client = MockTelegramClientWrapper(channel, posts)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'counts.json')

            await load_channel(
                client=mock_client,
                channel_id='@sample_channel',
                output_path=output_path
            )

            with open(output_path, 'r') as f:
                data = json.load(f)

            assert data['posts_count'] == 2
            assert data['comments_count'] == 3  # 2 on post 1, 1 on post 2
