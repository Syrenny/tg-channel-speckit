"""Contract tests for JSON output schema validation."""
import json
import os
import pytest
from datetime import datetime, timezone


def load_schema():
    """Load the JSON schema from contracts directory."""
    schema_path = os.path.join(
        os.path.dirname(__file__),
        '../../specs/002-channel-data-loader/contracts/channel-output.json'
    )
    with open(schema_path, 'r') as f:
        return json.load(f)


class TestOutputContract:
    """Contract tests for output JSON structure."""

    def test_valid_complete_output(self):
        """Valid complete output matches expected structure."""
        from src.models import Author, Comment, Post, Channel, OutputFile

        author = Author(user_id=1, username='u', first_name='F', last_name='L')
        comment = Comment(
            id=1,
            text='Test',
            date=datetime(2026, 2, 6, 12, 0, 0, tzinfo=timezone.utc),
            author=author
        )
        post = Post(
            id=1,
            text='Post',
            date=datetime(2026, 2, 6, 10, 0, 0, tzinfo=timezone.utc),
            views=100,
            comments=[comment]
        )
        channel = Channel(id=123, username='test', title='Test', posts=[post])
        output = OutputFile(
            version='1.0',
            status='complete',
            exported_at=datetime(2026, 2, 6, 15, 0, 0, tzinfo=timezone.utc),
            posts_count=1,
            comments_count=1,
            channel=channel
        )

        data = output.to_dict()

        # Verify required fields
        assert 'version' in data
        assert 'status' in data
        assert 'exported_at' in data
        assert 'posts_count' in data
        assert 'comments_count' in data
        assert 'channel' in data

        # Verify channel structure
        assert 'id' in data['channel']
        assert 'title' in data['channel']
        assert 'posts' in data['channel']

        # Verify post structure
        post_data = data['channel']['posts'][0]
        assert 'id' in post_data
        assert 'text' in post_data
        assert 'date' in post_data
        assert 'comments' in post_data

        # Verify comment structure
        comment_data = post_data['comments'][0]
        assert 'id' in comment_data
        assert 'text' in comment_data
        assert 'date' in comment_data
        assert 'author' in comment_data

        # Verify author structure
        author_data = comment_data['author']
        assert 'user_id' in author_data
        assert 'first_name' in author_data

    def test_valid_partial_output(self):
        """Partial output has correct status."""
        from src.models import Channel, OutputFile

        channel = Channel(id=123, username='test', title='Test', posts=[])
        output = OutputFile(
            version='1.0',
            status='partial',
            exported_at=datetime.now(timezone.utc),
            posts_count=0,
            comments_count=0,
            channel=channel
        )

        data = output.to_dict()
        assert data['status'] == 'partial'

    def test_status_enum_values(self):
        """Status only allows 'complete' or 'partial'."""
        from src.models import Channel, OutputFile

        channel = Channel(id=1, username='t', title='T', posts=[])

        # Valid statuses
        for status in ['complete', 'partial']:
            output = OutputFile(
                version='1.0',
                status=status,
                exported_at=datetime.now(timezone.utc),
                posts_count=0,
                comments_count=0,
                channel=channel
            )
            assert output.status == status

    def test_date_format_iso8601(self):
        """Dates are in ISO 8601 format."""
        from src.models import Channel, OutputFile

        channel = Channel(id=1, username='t', title='T', posts=[])
        output = OutputFile(
            version='1.0',
            status='complete',
            exported_at=datetime(2026, 2, 6, 15, 30, 45, tzinfo=timezone.utc),
            posts_count=0,
            comments_count=0,
            channel=channel
        )

        data = output.to_dict()
        # ISO 8601 format: YYYY-MM-DDTHH:MM:SS+00:00
        assert data['exported_at'] == '2026-02-06T15:30:45+00:00'

    def test_nullable_fields(self):
        """Optional fields can be null."""
        from src.models import Author, Channel, OutputFile

        # Author with null optional fields
        author = Author(user_id=1, username=None, first_name='F', last_name=None)
        data = author.to_dict()
        assert data['username'] is None
        assert data['last_name'] is None

        # Channel with null username
        channel = Channel(id=1, username=None, title='T', posts=[])
        data = channel.to_dict()
        assert data['username'] is None
