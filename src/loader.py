#!/usr/bin/env python3
"""
Channel Data Loader - Load posts and comments from Telegram channels.

Usage:
    python src/loader.py @channel_username
    python src/loader.py https://t.me/channel_username
"""
import argparse
import asyncio
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.config import ConfigError, load_config
from src.errors import AuthError, AccessError, NetworkError, LoaderError
from src.models import Channel, OutputFile
from src.telegram_client import TelegramClientWrapper, create_client
from src.utils import ensure_dir, format_error, print_error, print_progress, save_to_json


__version__ = '1.0.0'

# Output directory
OUTPUT_DIR = Path('.specify-for-tg-analysis/memory/channels')


async def load_channel(
    client: TelegramClientWrapper,
    channel_id: str,
    output_path: str,
    limit: Optional[int] = None,
) -> OutputFile:
    """
    Load channel data and save to JSON file.

    Args:
        client: Telegram client wrapper
        channel_id: Channel username or URL
        output_path: Path to save JSON output
        limit: Maximum number of posts to load

    Returns:
        OutputFile with loaded data
    """
    # Get channel info
    channel = await client.get_channel_info(channel_id)
    print_progress(f"Loading channel: {channel.title} (@{channel.username})")

    # Load posts
    posts = []
    total_comments = 0

    async for post in client.get_posts(channel, limit=limit):
        # Load comments for this post
        comments = []
        async for comment in client.get_comments(channel, post.id):
            comments.append(comment)

        post.comments = comments
        total_comments += len(comments)
        posts.append(post)

        print_progress(f"  Post {post.id}: {len(comments)} comments")

    channel.posts = posts

    # Create output
    output = OutputFile(
        version='1.0',
        status='complete',
        exported_at=datetime.now(timezone.utc),
        posts_count=len(posts),
        comments_count=total_comments,
        channel=channel
    )

    # Save to file
    save_to_json(output.to_dict(), output_path)
    print_progress(f"\nSaved to: {output_path}")
    print_progress(f"Total: {len(posts)} posts, {total_comments} comments")

    return output


def get_output_path(channel_id: str) -> str:
    """
    Get output file path for a channel.

    Args:
        channel_id: Channel username or URL

    Returns:
        Path to output JSON file
    """
    # Normalize channel name
    name = channel_id.replace('https://t.me/', '').lstrip('@')
    ensure_dir(str(OUTPUT_DIR))
    return str(OUTPUT_DIR / f"{name}.json")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Load posts and comments from a Telegram channel.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    %(prog)s @channel_username
    %(prog)s https://t.me/channel_username
    %(prog)s @channel --limit 100
'''
    )
    parser.add_argument(
        'channel',
        help='Channel username (with @) or URL'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Maximum number of posts to load'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing output file'
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    return parser.parse_args()


async def main_async(args: argparse.Namespace) -> int:
    """
    Main async entry point.

    Args:
        args: Parsed command line arguments

    Returns:
        Exit code (0=success, 1=error, 2=partial)
    """
    # Check if output file exists
    output_path = get_output_path(args.channel)
    if Path(output_path).exists() and not args.force:
        print_error(f"Output file already exists: {output_path}")
        print_error("Use --force to overwrite")
        return 1

    # Create client
    try:
        client = create_client()
    except ConfigError as e:
        print_error(format_error('ConfigError', str(e), e.args[0] if e.args else None))
        return 1

    # Connect and load
    try:
        await client.connect()
        await load_channel(
            client=client,
            channel_id=args.channel,
            output_path=output_path,
            limit=args.limit
        )
        return 0

    except AuthError as e:
        print_error(format_error('AuthError', e.message, e.suggestion))
        return 1

    except AccessError as e:
        print_error(format_error('AccessError', e.message, e.suggestion))
        return 1

    except NetworkError as e:
        print_error(format_error('NetworkError', e.message, e.suggestion))
        return 1

    except LoaderError as e:
        print_error(format_error('LoaderError', str(e)))
        return 1

    except KeyboardInterrupt:
        print_error("\nInterrupted by user")
        return 2

    finally:
        await client.disconnect()


def main() -> int:
    """Main entry point."""
    args = parse_args()
    return asyncio.run(main_async(args))


if __name__ == '__main__':
    sys.exit(main())
