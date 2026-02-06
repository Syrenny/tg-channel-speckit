# tg-channel-speckit

Loads data from Telegram channels and finds the most relevant potential users for your product based on their activity and engagement in thematic channels.

## Features

- Load all posts and comments from a Telegram channel
- Hierarchical data structure: Channel -> Posts -> Comments -> Authors
- Automatic rate limiting and retry (Telegram FloodWait handling)
- Partial export support — saves progress on interruption
- JSON output with metadata (version, status, export timestamp)
- Identify potential users for your product based on their activity in relevant channels

## Prerequisites

- Python 3.13+
- Telegram API credentials ([get them here](https://my.telegram.org))

## Installation

```bash
git clone git@github.com:Syrenny/tg-channel-speckit.git
cd tg-channel-speckit
pip install -r requirements.txt
```

Or using [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

## Configuration

Copy the example environment file and fill in your Telegram API credentials:

```bash
cp .env.example .env
```

```env
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
```

On first run, you will be prompted to authorize with your phone number and confirmation code. The session is saved automatically in `.specify-for-tg-analysis/tg/` (gitignored).

## Usage

```bash
# Load all posts and comments from a channel
python src/loader.py @channel_username

# Using channel URL
python src/loader.py https://t.me/channel_username

# Limit number of posts
python src/loader.py @channel --limit 100

# Overwrite existing output
python src/loader.py @channel --force
```

Output is saved to `.specify-for-tg-analysis/memory/channels/{channel_name}.json`.

### Output format

```json
{
  "version": "1.0",
  "status": "complete",
  "exported_at": "2026-02-06T15:30:00Z",
  "posts_count": 42,
  "comments_count": 156,
  "channel": {
    "id": 1234567890,
    "username": "example_channel",
    "title": "Example Channel",
    "posts": [
      {
        "id": 1,
        "text": "Post text",
        "date": "2026-01-15T10:00:00Z",
        "views": 500,
        "comments": [
          {
            "id": 1,
            "text": "Comment text",
            "date": "2026-01-15T10:05:00Z",
            "author": {
              "user_id": 123,
              "username": "user",
              "first_name": "John",
              "last_name": "Doe"
            }
          }
        ]
      }
    ]
  }
}
```

## Project structure

```
src/
├── loader.py            # Main loader script (entry point)
├── models.py            # Dataclasses: Channel, Post, Comment, Author
├── telegram_client.py   # Telethon wrapper with rate limiting
├── config.py            # .env configuration loading
├── errors.py            # Custom exception classes
└── utils.py             # Helpers: progress, file I/O

tests/
├── unit/                # Unit tests for models, config, utils, contracts
├── integration/         # Integration tests with mocked Telegram client
└── fixtures/            # Test fixtures and mocks
```

## Testing

```bash
pytest
```

## License

MIT
