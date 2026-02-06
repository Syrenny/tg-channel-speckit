# Data Model: Channel Data Loader

**Date**: 2026-02-06
**Feature**: 002-channel-data-loader

## Entities

### Channel

Корневая сущность, представляющая Telegram канал.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | integer | yes | Уникальный Telegram ID канала |
| username | string | no | @username канала (может отсутствовать) |
| title | string | yes | Отображаемое название канала |
| posts | Post[] | yes | Список постов (может быть пустым) |

### Post

Сообщение в канале.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | integer | yes | ID сообщения в канале |
| text | string | yes | Текст поста (пустая строка если только медиа) |
| date | string (ISO 8601) | yes | Дата публикации |
| views | integer | no | Количество просмотров |
| comments | Comment[] | yes | Список комментариев (может быть пустым) |

### Comment

Комментарий к посту.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | integer | yes | ID комментария |
| text | string | yes | Текст комментария |
| date | string (ISO 8601) | yes | Дата комментария |
| author | Author | yes | Информация об авторе |

### Author

Пользователь Telegram.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| user_id | integer | yes | Telegram user ID |
| username | string | no | @username (null если скрыт/отсутствует) |
| first_name | string | yes | Имя пользователя |
| last_name | string | no | Фамилия (null если отсутствует) |

### OutputFile (Metadata wrapper)

Обёртка для выходного JSON файла.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| version | string | yes | Версия формата (e.g., "1.0") |
| status | enum | yes | "complete" \| "partial" |
| exported_at | string (ISO 8601) | yes | Время экспорта |
| posts_count | integer | yes | Количество загруженных постов |
| comments_count | integer | yes | Общее количество комментариев |
| channel | Channel | yes | Данные канала |

## Relationships

```
OutputFile
└── Channel (1:1)
    └── Post (1:N)
        └── Comment (1:N)
            └── Author (N:1, embedded)
```

## Validation Rules

1. **Channel.id**: Положительное целое число
2. **Post.id**: Уникален в пределах канала
3. **Comment.id**: Уникален в пределах поста
4. **date fields**: Валидный ISO 8601 формат с timezone
5. **Author.user_id**: Положительное целое число
6. **status**: Только "complete" или "partial"

## State Transitions

```
[Start] → Загрузка → [Complete]
                  ↘
           Прерывание → [Partial]
```

При статусе "partial":
- Файл содержит все успешно загруженные данные
- `posts_count` отражает реальное количество в файле
- Пользователь может запустить повторно с `--force`

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
    "posts": [
      {
        "id": 100,
        "text": "Hello world!",
        "date": "2026-02-01T10:00:00Z",
        "views": 1500,
        "comments": [
          {
            "id": 1,
            "text": "Great post!",
            "date": "2026-02-01T10:05:00Z",
            "author": {
              "user_id": 987654321,
              "username": "commenter",
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
