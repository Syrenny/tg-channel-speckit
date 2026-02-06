# Tasks: Channel Data Loader

**Input**: Design documents from `/specs/002-channel-data-loader/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: TDD is NON-NEGOTIABLE per constitution. Tests are written BEFORE implementation.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1, US2, US3 - maps to user stories from spec.md

## Path Conventions

- Source: `src/` at repository root
- Tests: `tests/` at repository root
- Output: `.specify-for-tg-analysis/memory/channels/`
- Session: `.specify-for-tg-analysis/tg/`

---

## Phase 1: Setup (Shared Infrastructure) ✅

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure: src/, tests/unit/, tests/integration/, tests/fixtures/
- [x] T002 Create requirements.txt with telethon>=1.34.0, python-dotenv>=1.0.0, pytest>=8.0.0
- [x] T003 [P] Create .env.example with TELEGRAM_API_ID and TELEGRAM_API_HASH placeholders
- [x] T004 [P] Update .gitignore to include .specify-for-tg-analysis/tg/, .env, __pycache__/
- [x] T005 [P] Create pytest.ini with asyncio mode configuration

---

## Phase 2: Foundational (Blocking Prerequisites) ✅

**Purpose**: Core infrastructure that MUST be complete before ANY user story

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Tests for Foundation

- [x] T006 [P] Unit test for config loading in tests/unit/test_config.py
- [x] T007 [P] Unit test for error utilities in tests/unit/test_utils.py

### Implementation

- [x] T008 Implement config loader (read .env, validate required vars) in src/config.py
- [x] T009 [P] Implement error classes (AuthError, AccessError, NetworkError) in src/errors.py
- [x] T010 [P] Implement utility functions (ensure_dir, format_error) in src/utils.py
- [x] T011 Create output directories: .specify-for-tg-analysis/memory/channels/ and .specify-for-tg-analysis/tg/

**Checkpoint**: Foundation ready - user story implementation can now begin ✅

---

## Phase 3: User Story 1 - Load Channel Data to File (Priority: P1) 🎯 MVP ✅

**Goal**: Загрузить посты и комментарии из Telegram канала в JSON файл

**Independent Test**: Запустить `python src/loader.py @channel` и проверить созданный JSON файл

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T012 [P] [US1] Unit test for Author dataclass in tests/unit/test_models.py
- [x] T013 [P] [US1] Unit test for Comment dataclass in tests/unit/test_models.py
- [x] T014 [P] [US1] Unit test for Post dataclass in tests/unit/test_models.py
- [x] T015 [P] [US1] Unit test for Channel dataclass in tests/unit/test_models.py
- [x] T016 [P] [US1] Unit test for OutputFile dataclass in tests/unit/test_models.py
- [x] T017 [P] [US1] Create mock Telegram client fixture in tests/fixtures/mock_telegram.py
- [x] T018 [US1] Integration test for basic channel loading in tests/integration/test_loader.py
- [x] T019 [US1] Contract test: validate JSON output against schema in tests/unit/test_contracts.py

### Implementation for User Story 1

- [x] T020 [P] [US1] Create Author dataclass with user_id, username, first_name, last_name in src/models.py
- [x] T021 [P] [US1] Create Comment dataclass with id, text, date, author in src/models.py
- [x] T022 [P] [US1] Create Post dataclass with id, text, date, views, comments in src/models.py
- [x] T023 [P] [US1] Create Channel dataclass with id, username, title, posts in src/models.py
- [x] T024 [US1] Create OutputFile dataclass with version, status, exported_at, counts, channel in src/models.py
- [x] T025 [US1] Implement to_dict() method for all dataclasses in src/models.py
- [x] T026 [US1] Implement TelegramClient wrapper with connect/disconnect in src/telegram_client.py
- [x] T027 [US1] Implement get_channel_info() method in src/telegram_client.py
- [x] T028 [US1] Implement get_posts() async generator in src/telegram_client.py
- [x] T029 [US1] Implement get_comments(post_id) async generator in src/telegram_client.py
- [x] T030 [US1] Implement save_to_json(output_file, path) in src/utils.py
- [x] T031 [US1] Implement main loader logic in src/loader.py
- [x] T032 [US1] Add CLI argument parsing (channel, --help, --version) in src/loader.py
- [x] T033 [US1] Add basic error handling for auth and access errors in src/loader.py

**Checkpoint**: User Story 1 complete - can load channel data to JSON file ✅

---

## Phase 4: User Story 2 - Preserve Data Hierarchy (Priority: P2)

**Goal**: Гарантировать иерархическую структуру данных (channel → posts → comments → authors)

**Independent Test**: Проверить JSON файл на соответствие схеме из contracts/channel-output.json

### Tests for User Story 2

- [ ] T034 [P] [US2] Unit test for JSON schema validation in tests/unit/test_contracts.py
- [ ] T035 [US2] Integration test: verify hierarchy in output file in tests/integration/test_hierarchy.py

### Implementation for User Story 2

- [ ] T036 [US2] Add JSON schema validation to OutputFile.validate() in src/models.py
- [ ] T037 [US2] Ensure author info is embedded in each comment in src/telegram_client.py
- [ ] T038 [US2] Add validation before save (check required fields) in src/loader.py

**Checkpoint**: User Story 2 complete - data hierarchy is guaranteed

---

## Phase 5: User Story 3 - Handle Large Channels (Priority: P3)

**Goal**: Поддержка больших каналов с прогресс-индикацией и rate limiting

**Independent Test**: Запустить загрузку канала с 500+ постами, проверить прогресс и корректное завершение

### Tests for User Story 3

- [ ] T039 [P] [US3] Unit test for progress indicator in tests/unit/test_utils.py
- [ ] T040 [P] [US3] Unit test for rate limiting handler in tests/unit/test_telegram_client.py
- [ ] T041 [US3] Integration test: partial save on interruption in tests/integration/test_partial.py

### Implementation for User Story 3

- [ ] T042 [US3] Implement progress indicator (posts/comments counters) in src/utils.py
- [ ] T043 [US3] Add progress display to loader main loop in src/loader.py
- [ ] T044 [US3] Implement FloodWait handling with exponential backoff in src/telegram_client.py
- [ ] T045 [US3] Add --limit flag to CLI for restricting post count in src/loader.py
- [ ] T046 [US3] Implement partial save on KeyboardInterrupt/exception in src/loader.py
- [ ] T047 [US3] Add --force flag to overwrite existing files in src/loader.py
- [ ] T048 [US3] Set status="partial" in metadata when interrupted in src/loader.py

**Checkpoint**: User Story 3 complete - handles large channels gracefully

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T049 [P] Verify all tests pass with pytest in tests/
- [ ] T050 [P] Validate quickstart.md instructions work end-to-end
- [ ] T051 Add --json-schema flag to output schema for validation in src/loader.py
- [ ] T052 Add proper exit codes: 0 (success), 1 (error), 2 (partial) in src/loader.py
- [ ] T053 Code cleanup: remove debug prints, add docstrings

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - MVP milestone
- **User Story 2 (Phase 4)**: Depends on US1 completion (extends validation)
- **User Story 3 (Phase 5)**: Depends on US1 completion (extends handling)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

```
Phase 1: Setup
    ↓
Phase 2: Foundational
    ↓
Phase 3: US1 (MVP) ←── STOP HERE FOR MVP
    ↓
Phase 4: US2 (can start after US1)
    ↓
Phase 5: US3 (can start after US1, parallel to US2)
    ↓
Phase 6: Polish
```

### Within Each User Story

1. Tests MUST be written and FAIL before implementation
2. Models before client methods
3. Client methods before loader logic
4. Core implementation before CLI flags

### Parallel Opportunities

- T003, T004, T005 can run in parallel (Setup)
- T006, T007 can run in parallel (Foundation tests)
- T009, T010 can run in parallel (Foundation impl)
- T012-T017 can run in parallel (US1 model tests)
- T020-T023 can run in parallel (US1 model impl)
- T034 can run parallel to T035 (US2 tests)
- T039, T040 can run in parallel (US3 tests)
- T049, T050 can run in parallel (Polish)

---

## Parallel Example: User Story 1 Models

```bash
# Launch all model tests in parallel:
Task: "Unit test for Author dataclass in tests/unit/test_models.py"
Task: "Unit test for Comment dataclass in tests/unit/test_models.py"
Task: "Unit test for Post dataclass in tests/unit/test_models.py"
Task: "Unit test for Channel dataclass in tests/unit/test_models.py"

# After tests written, launch all model implementations in parallel:
Task: "Create Author dataclass in src/models.py"
Task: "Create Comment dataclass in src/models.py"
Task: "Create Post dataclass in src/models.py"
Task: "Create Channel dataclass in src/models.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T011)
3. Complete Phase 3: User Story 1 (T012-T033)
4. **STOP and VALIDATE**: Run `python src/loader.py @test_channel`
5. Verify JSON file created with correct structure

### Incremental Delivery

1. **MVP**: Setup + Foundational + US1 → Basic channel loading works
2. **v1.1**: Add US2 → Data hierarchy validated
3. **v1.2**: Add US3 → Large channels supported, progress shown
4. **v1.3**: Polish → Documentation, cleanup

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story
- TDD is mandatory: write test → verify fails → implement → verify passes
- Commit after each task or logical group
- Stop at any checkpoint to validate independently
- Session file in .specify-for-tg-analysis/tg/ - NEVER commit to git
