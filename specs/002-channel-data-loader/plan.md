# Implementation Plan: Channel Data Loader

**Branch**: `002-channel-data-loader` | **Date**: 2026-02-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-channel-data-loader/spec.md`

## Summary

CLI-скрипт для загрузки постов, комментариев и авторов из Telegram канала в
иерархическую JSON-структуру. Один канал = один файл. Использует Telegram API
через библиотеку Telethon. Поддерживает rate limiting, partial saves и
переиспользование сессий авторизации.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Telethon (Telegram API), python-dotenv (.env parsing)
**Storage**: JSON файлы в `.specify-for-tg-analysis/memory/channels/`
**Testing**: pytest с мокированием Telegram API
**Target Platform**: Linux (macOS опционально)
**Project Type**: Single CLI tool
**Performance Goals**: 100 постов < 5 минут (с учётом rate limiting)
**Constraints**: Graceful rate limiting, partial data recovery
**Scale/Scope**: Каналы до 10000+ постов

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Test-Driven Development ✅

- [ ] Тесты пишутся ДО реализации
- [ ] Используем pytest с fixtures для мокирования Telegram API
- [ ] Контрактные тесты для JSON-структуры выхода
- [ ] Integration тесты с реальным (тестовым) каналом

### II. CLI-First Interface ✅

- [ ] Вход: аргументы командной строки (channel URL/username, --limit, --force)
- [ ] Выход: stdout для прогресса, stderr для ошибок
- [ ] JSON-файл как основной артефакт
- [ ] Поддержка --help, --version
- [ ] Exit codes: 0 (success), 1 (error), 2 (partial)

### III. Simplicity (YAGNI) ✅

- [ ] Минимум зависимостей (только Telethon + dotenv)
- [ ] Один скрипт = одна задача (загрузка канала)
- [ ] Никаких абстрактных фабрик или сложных паттернов
- [ ] Плоская структура проекта

### Technology Deviation (Justified)

| Deviation | Justification |
|-----------|---------------|
| Python вместо Bash | Telegram API требует асинхронную библиотеку; Bash не может работать с MTProto протоколом |
| Telethon зависимость | Единственный способ получить доступ к Telegram API; минимальная и стабильная библиотека |

## Project Structure

### Documentation (this feature)

```text
specs/002-channel-data-loader/
├── plan.md              # This file
├── research.md          # Phase 0: технические решения
├── data-model.md        # Phase 1: структура данных
├── quickstart.md        # Phase 1: как запустить
├── contracts/           # Phase 1: JSON schema
│   └── channel-output.json
└── tasks.md             # Phase 2: задачи реализации
```

### Source Code (repository root)

```text
src/
├── loader.py            # Основной скрипт загрузки
├── models.py            # Dataclasses для Channel, Post, Comment, Author
├── telegram_client.py   # Обёртка над Telethon
└── utils.py             # Helpers: progress, error handling

tests/
├── unit/
│   ├── test_models.py
│   └── test_utils.py
├── integration/
│   └── test_loader.py
└── fixtures/
    └── mock_telegram.py

.env.example             # Шаблон для credentials
.gitignore               # Включает .specify-for-tg-analysis/tg/
```

**Structure Decision**: Single project structure. Простой CLI-инструмент не требует
разделения на frontend/backend. Все файлы в одном `src/` каталоге.

## Complexity Tracking

> Нет нарушений, требующих обоснования. Структура минимальна.
