# tg-channel-speckit Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-02-06

## Active Technologies

- Python 3.11+ + Telethon (Telegram API), python-dotenv (.env parsing) (002-channel-data-loader)

## Project Structure

```text
src/
├── loader.py            # Main loader script
├── models.py            # Dataclasses for Channel, Post, Comment, Author
├── telegram_client.py   # Telethon wrapper
└── utils.py             # Helpers: progress, error handling

tests/
├── unit/
├── integration/
└── fixtures/
```

## Commands

```bash
# Run loader
python src/loader.py @channel_username

# Run tests
pytest

# Lint
ruff check .
```

## Code Style

- Python 3.11+: Follow PEP 8
- Use type hints
- Async/await for Telegram API calls

## Recent Changes

- 002-channel-data-loader: Added Python 3.11+ + Telethon (Telegram API), python-dotenv (.env parsing)

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
