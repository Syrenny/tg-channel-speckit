# Research: Channel Data Loader

**Date**: 2026-02-06
**Feature**: 002-channel-data-loader

## Decision Log

### 1. Telegram API Library

**Decision**: Telethon

**Rationale**:
- Полная поддержка MTProto (нативный протокол Telegram)
- Асинхронный API для эффективной работы с rate limits
- Активно поддерживается, стабильный API
- Доступ к комментариям через `client.iter_messages(channel, reply_to=post_id)`

**Alternatives Considered**:
- `python-telegram-bot`: Только Bot API, нет доступа к комментариям каналов
- `Pyrogram`: Аналогичен Telethon, но менее документирован
- `tdlib`: C++ библиотека, избыточная сложность для простого скрипта

### 2. Авторизация и сессии

**Decision**: Файл сессии Telethon в `.specify-for-tg-analysis/tg/session.session`

**Rationale**:
- Telethon автоматически сохраняет сессию в SQLite файл
- Избегаем повторной авторизации (SMS/2FA) при каждом запуске
- Директория исключена из Git для безопасности

**Implementation**:
```python
client = TelegramClient(
    '.specify-for-tg-analysis/tg/session',
    api_id,
    api_hash
)
```

### 3. Rate Limiting Strategy

**Decision**: Exponential backoff с базовой задержкой 1 секунда

**Rationale**:
- Telegram возвращает `FloodWaitError` с временем ожидания
- Telethon автоматически обрабатывает FloodWait если включен `flood_sleep_threshold`
- Дополнительная задержка между запросами предотвращает блокировки

**Implementation**:
```python
client.flood_sleep_threshold = 60  # Автоматически ждать до 60 сек
# Между запросами: await asyncio.sleep(0.5)
```

### 4. Формат выходного файла

**Decision**: JSON с иерархической структурой

**Rationale**:
- Машиночитаемый формат
- Легко парсится Python/jq/другими инструментами
- Поддерживает вложенные структуры (channel → posts → comments)
- Совместим с LLM-контекстом

**Schema**: См. `contracts/channel-output.json`

### 5. Partial Save Strategy

**Decision**: Сохранять при прерывании с `"status": "partial"` в метаданных

**Rationale**:
- Для больших каналов потеря прогресса критична
- Пользователь видит что загружено и откуда продолжить
- Простая реализация через try/finally

**Implementation**:
```python
try:
    # загрузка
finally:
    save_data(data, status="partial" if interrupted else "complete")
```

### 6. Обработка отсутствующих данных

**Decision**: Nullable поля, пустые списки

**Rationale**:
- Username может отсутствовать у пользователей Telegram
- Посты могут не иметь комментариев
- JSON schema допускает null для опциональных полей

**Rules**:
- `username`: `string | null`
- `comments`: `[]` если нет комментариев
- `text`: `""` если пост содержит только медиа

## Open Questions (Resolved)

| Question | Resolution |
|----------|------------|
| Где хранить файлы? | `.specify-for-tg-analysis/memory/channels/` |
| Где хранить сессию? | `.specify-for-tg-analysis/tg/` |
| Что делать при прерывании? | Сохранять partial данные |

## Dependencies

```
telethon>=1.34.0
python-dotenv>=1.0.0
```

## References

- [Telethon Documentation](https://docs.telethon.dev/)
- [Telegram API Rate Limits](https://core.telegram.org/api/errors#420-flood)
- [MTProto Protocol](https://core.telegram.org/mtproto)
