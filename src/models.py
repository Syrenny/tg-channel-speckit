"""Data models for the channel loader."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Author:
    """Telegram user who authored a comment."""
    user_id: int
    username: Optional[str]
    first_name: str
    last_name: Optional[str]

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }


@dataclass
class Comment:
    """Comment on a channel post."""
    id: int
    text: str
    date: datetime
    author: Author

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'text': self.text,
            'date': self.date.isoformat(),
            'author': self.author.to_dict(),
        }


@dataclass
class Post:
    """Post in a Telegram channel."""
    id: int
    text: str
    date: datetime
    views: Optional[int]
    comments: list[Comment] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'text': self.text,
            'date': self.date.isoformat(),
            'views': self.views,
            'comments': [c.to_dict() for c in self.comments],
        }


@dataclass
class Channel:
    """Telegram channel."""
    id: int
    username: Optional[str]
    title: str
    posts: list[Post] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'username': self.username,
            'title': self.title,
            'posts': [p.to_dict() for p in self.posts],
        }


@dataclass
class OutputFile:
    """Output file wrapper with metadata."""
    version: str
    status: str  # 'complete' or 'partial'
    exported_at: datetime
    posts_count: int
    comments_count: int
    channel: Channel

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'version': self.version,
            'status': self.status,
            'exported_at': self.exported_at.isoformat(),
            'posts_count': self.posts_count,
            'comments_count': self.comments_count,
            'channel': self.channel.to_dict(),
        }
