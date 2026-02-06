"""Unit tests for data models."""
from datetime import datetime, timezone
import pytest


class TestAuthor:
    """Tests for Author dataclass."""

    def test_author_creation_full(self):
        """Author created with all fields."""
        from src.models import Author

        author = Author(
            user_id=12345,
            username='testuser',
            first_name='John',
            last_name='Doe'
        )
        assert author.user_id == 12345
        assert author.username == 'testuser'
        assert author.first_name == 'John'
        assert author.last_name == 'Doe'

    def test_author_creation_minimal(self):
        """Author created with only required fields."""
        from src.models import Author

        author = Author(
            user_id=12345,
            username=None,
            first_name='John',
            last_name=None
        )
        assert author.user_id == 12345
        assert author.username is None
        assert author.first_name == 'John'
        assert author.last_name is None

    def test_author_to_dict(self):
        """Author converts to dict correctly."""
        from src.models import Author

        author = Author(
            user_id=12345,
            username='testuser',
            first_name='John',
            last_name='Doe'
        )
        d = author.to_dict()
        assert d['user_id'] == 12345
        assert d['username'] == 'testuser'
        assert d['first_name'] == 'John'
        assert d['last_name'] == 'Doe'


class TestComment:
    """Tests for Comment dataclass."""

    def test_comment_creation(self):
        """Comment created with all fields."""
        from src.models import Author, Comment

        author = Author(user_id=1, username='u', first_name='F', last_name=None)
        comment = Comment(
            id=100,
            text='Hello',
            date=datetime(2026, 2, 6, 12, 0, 0, tzinfo=timezone.utc),
            author=author
        )
        assert comment.id == 100
        assert comment.text == 'Hello'
        assert comment.author.user_id == 1

    def test_comment_to_dict(self):
        """Comment converts to dict with nested author."""
        from src.models import Author, Comment

        author = Author(user_id=1, username='u', first_name='F', last_name=None)
        comment = Comment(
            id=100,
            text='Hello',
            date=datetime(2026, 2, 6, 12, 0, 0, tzinfo=timezone.utc),
            author=author
        )
        d = comment.to_dict()
        assert d['id'] == 100
        assert d['text'] == 'Hello'
        assert d['date'] == '2026-02-06T12:00:00+00:00'
        assert d['author']['user_id'] == 1


class TestPost:
    """Tests for Post dataclass."""

    def test_post_creation(self):
        """Post created with all fields."""
        from src.models import Post

        post = Post(
            id=10,
            text='Post content',
            date=datetime(2026, 2, 6, 10, 0, 0, tzinfo=timezone.utc),
            views=1500,
            comments=[]
        )
        assert post.id == 10
        assert post.text == 'Post content'
        assert post.views == 1500
        assert post.comments == []

    def test_post_with_comments(self):
        """Post with nested comments."""
        from src.models import Author, Comment, Post

        author = Author(user_id=1, username='u', first_name='F', last_name=None)
        comment = Comment(id=1, text='Hi', date=datetime.now(timezone.utc), author=author)
        post = Post(
            id=10,
            text='Post',
            date=datetime.now(timezone.utc),
            views=100,
            comments=[comment]
        )
        assert len(post.comments) == 1
        assert post.comments[0].author.user_id == 1

    def test_post_to_dict(self):
        """Post converts to dict with nested comments."""
        from src.models import Author, Comment, Post

        author = Author(user_id=1, username='u', first_name='F', last_name=None)
        comment = Comment(
            id=1,
            text='Hi',
            date=datetime(2026, 2, 6, 12, 0, 0, tzinfo=timezone.utc),
            author=author
        )
        post = Post(
            id=10,
            text='Post',
            date=datetime(2026, 2, 6, 10, 0, 0, tzinfo=timezone.utc),
            views=100,
            comments=[comment]
        )
        d = post.to_dict()
        assert d['id'] == 10
        assert len(d['comments']) == 1
        assert d['comments'][0]['author']['user_id'] == 1


class TestChannel:
    """Tests for Channel dataclass."""

    def test_channel_creation(self):
        """Channel created with all fields."""
        from src.models import Channel

        channel = Channel(
            id=123456789,
            username='testchannel',
            title='Test Channel',
            posts=[]
        )
        assert channel.id == 123456789
        assert channel.username == 'testchannel'
        assert channel.title == 'Test Channel'

    def test_channel_to_dict(self):
        """Channel converts to dict."""
        from src.models import Channel

        channel = Channel(
            id=123456789,
            username='testchannel',
            title='Test Channel',
            posts=[]
        )
        d = channel.to_dict()
        assert d['id'] == 123456789
        assert d['username'] == 'testchannel'
        assert d['posts'] == []


class TestOutputFile:
    """Tests for OutputFile dataclass."""

    def test_output_file_creation(self):
        """OutputFile created with all fields."""
        from src.models import Channel, OutputFile

        channel = Channel(id=1, username='c', title='C', posts=[])
        output = OutputFile(
            version='1.0',
            status='complete',
            exported_at=datetime(2026, 2, 6, 15, 0, 0, tzinfo=timezone.utc),
            posts_count=10,
            comments_count=50,
            channel=channel
        )
        assert output.version == '1.0'
        assert output.status == 'complete'
        assert output.posts_count == 10

    def test_output_file_partial_status(self):
        """OutputFile with partial status."""
        from src.models import Channel, OutputFile

        channel = Channel(id=1, username='c', title='C', posts=[])
        output = OutputFile(
            version='1.0',
            status='partial',
            exported_at=datetime.now(timezone.utc),
            posts_count=5,
            comments_count=20,
            channel=channel
        )
        assert output.status == 'partial'

    def test_output_file_to_dict(self):
        """OutputFile converts to dict with nested channel."""
        from src.models import Channel, OutputFile

        channel = Channel(id=1, username='c', title='C', posts=[])
        output = OutputFile(
            version='1.0',
            status='complete',
            exported_at=datetime(2026, 2, 6, 15, 0, 0, tzinfo=timezone.utc),
            posts_count=10,
            comments_count=50,
            channel=channel
        )
        d = output.to_dict()
        assert d['version'] == '1.0'
        assert d['status'] == 'complete'
        assert d['exported_at'] == '2026-02-06T15:00:00+00:00'
        assert d['channel']['id'] == 1
