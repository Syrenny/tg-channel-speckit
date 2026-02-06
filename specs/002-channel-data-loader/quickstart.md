# Quickstart: Channel Data Loader

## Prerequisites

1. Python 3.11+
2. Telegram API credentials (получить на https://my.telegram.org)

## Setup

### 1. Clone and install dependencies

```bash
cd tg-channel-speckit
pip install -r requirements.txt
```

### 2. Configure credentials

Создайте `.env` файл в корне проекта:

```bash
cp .env.example .env
```

Заполните credentials:

```env
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
```

### 3. First run (authorization)

При первом запуске потребуется авторизация:

```bash
python src/loader.py @channel_username
```

Введите номер телефона и код подтверждения. Сессия сохранится автоматически.

## Usage

### Basic usage

```bash
# Загрузить все посты и комментарии
python src/loader.py @channel_username

# Указать URL канала
python src/loader.py https://t.me/channel_username
```

### Options

```bash
# Ограничить количество постов
python src/loader.py @channel --limit 100

# Перезаписать существующий файл
python src/loader.py @channel --force

# Показать помощь
python src/loader.py --help
```

### Output

Файл сохраняется в:
```
.specify-for-tg-analysis/memory/channels/{channel_username}.json
```

## Example Output

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
    "posts": [...]
  }
}
```

## Troubleshooting

### "FloodWaitError"

Telegram rate limiting. Скрипт автоматически ждёт и продолжает.

### "ChannelPrivateError"

Канал приватный. Убедитесь, что ваш аккаунт подписан на канал.

### "ApiIdInvalidError"

Неверные credentials. Проверьте `.env` файл.

### Partial data saved

Соединение прервалось. Данные сохранены с `"status": "partial"`.
Запустите повторно с `--force` для полной загрузки.

## File Locations

| Path | Description |
|------|-------------|
| `.env` | API credentials |
| `.specify-for-tg-analysis/tg/` | Session file (gitignored) |
| `.specify-for-tg-analysis/memory/channels/` | Output JSON files |
