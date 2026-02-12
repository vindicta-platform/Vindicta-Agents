# Tasks: Chainlit UI with SQLite Persistence

**Input**: Design documents from `/specs/010-chainlit-sqlite-persistence/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: Tests are included per Constitution Principle QG-2 (≥90% coverage) and the TDD mandate.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and persistent storage directory

- [ ] T001 Create `vault/` directory at repo root for SQLite storage
- [ ] T002 Add `vault/` to `.gitignore` to exclude persistent state from version control
- [ ] T003 [P] Create `src/vindicta_agents/ui/__init__.py` if not present (ensure package importability)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Refactor nexus.py to support injectable checkpointer — MUST complete before ANY user story

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Refactor `build_master_graph()` in `src/vindicta_agents/swarm/nexus.py` to accept optional `checkpointer` parameter (default: `MemorySaver()`)
- [ ] T005 Update module-level `vindicta_swarm` export to continue using `MemorySaver()` for backward compatibility
- [ ] T006 [P] Write unit test for checkpointer injection in `tests/unit/test_persistence.py` — verify `build_master_graph(checkpointer=MemorySaver())` compiles without error
- [ ] T007 [P] Write unit test verifying `build_master_graph()` defaults to `MemorySaver()` when no checkpointer is provided in `tests/unit/test_persistence.py`
- [ ] T008 Run existing tests (`uv run pytest tests/unit/ -v`) to confirm no regressions from nexus refactor

**Checkpoint**: Foundation ready — nexus accepts injectable checkpointer, all existing tests pass

---

## Phase 3: User Story 1 — Persistent Swarm Memory (Priority: P1) 🎯 MVP

**Goal**: Swarm state persists to SQLite and survives process restarts

**Independent Test**: Invoke swarm → stop process → restart → verify state is recoverable

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T009 [P] [US1] Write unit test in `tests/unit/test_persistence.py` — verify `SqliteSaver` initializes and creates tables in a temp SQLite file
- [ ] T010 [P] [US1] Write unit test in `tests/unit/test_persistence.py` — verify state round-trip: write state via `build_master_graph(checkpointer=SqliteSaver(...))`, invoke, then read back and assert state matches
- [ ] T011 [P] [US1] Write unit test in `tests/unit/test_persistence.py` — verify fallback to `MemorySaver` when SQLite connection fails (corrupt path), with warning logged
- [ ] T012 [US1] Write BDD scenario in `features/persistence.feature` — "Swarm state survives process restart"

### Implementation for User Story 1

- [ ] T013 [US1] Create persistence helper module `src/vindicta_agents/ui/persistence.py` with `create_checkpointer(db_path: str) -> BaseCheckpointSaver` function
- [ ] T014 [US1] Implement fallback logic in `create_checkpointer()`: try `SqliteSaver`, catch exceptions, log warning via structlog, return `MemorySaver`
- [ ] T015 [US1] Update `src/vindicta_agents/ui/app.py` to import and use `create_checkpointer("vault/swarm_state.sqlite")` instead of ephemeral swarm
- [ ] T016 [US1] Update `src/vindicta_agents/ui/app.py` to pass the checkpointer to `build_master_graph(checkpointer=saver)`
- [ ] T017 [US1] Run all User Story 1 tests and verify they pass

**Checkpoint**: Swarm state survives restarts via SQLite. MVP is functional.

---

## Phase 4: User Story 2 — Daily Thread Management (Priority: P1)

**Goal**: Date-keyed thread IDs ensure same-day workflows share context

**Independent Test**: Two messages on the same day use the same thread; different days use different threads

### Tests for User Story 2 ⚠️

- [ ] T018 [P] [US2] Write unit test in `tests/unit/test_persistence.py` — verify `get_daily_thread_id()` returns `daily-YYYY-MM-DD` format for today
- [ ] T019 [P] [US2] Write unit test in `tests/unit/test_persistence.py` — verify `get_daily_thread_id()` returns consistent value when called multiple times on the same day
- [ ] T020 [US2] Write BDD scenario in `features/persistence.feature` — "Same-day workflows share a daily thread"

### Implementation for User Story 2

- [ ] T021 [US2] Implement `get_daily_thread_id() -> str` in `src/vindicta_agents/ui/persistence.py` returning `daily-YYYY-MM-DD`
- [ ] T022 [US2] Update `@cl.on_chat_start` in `src/vindicta_agents/ui/app.py` to use `get_daily_thread_id()` instead of `uuid.uuid4()`
- [ ] T023 [US2] Update the session greeting message to display the current daily thread ID
- [ ] T024 [US2] Run all User Story 2 tests and verify they pass

**Checkpoint**: Daily threads operational. All same-day workflows share a single persistent thread.

---

## Phase 5: User Story 3 — Playbook Quick Actions (Priority: P2)

**Goal**: Quick-action buttons for playbook workflows in the Chainlit interface

**Independent Test**: Launch UI, verify buttons appear, click one, confirm intent is dispatched

### Tests for User Story 3 ⚠️

- [ ] T025 [P] [US3] Write unit test in `tests/unit/test_playbook_actions.py` — verify `get_playbook_actions()` returns a list of at least 5 actions
- [ ] T026 [P] [US3] Write unit test in `tests/unit/test_playbook_actions.py` — verify each action has `name`, `label`, and `description` fields

### Implementation for User Story 3

- [ ] T027 [P] [US3] Create `src/vindicta_agents/ui/playbook_actions.py` with `PLAYBOOK_ACTIONS` list defining quick-actions for: `/sm-check-in`, `/adl-standup`, `/adl-pr-review`, `/po-roadmap-update`, `/sm-end-day`
- [ ] T028 [US3] Implement `get_playbook_actions() -> list[dict]` in `playbook_actions.py` returning Chainlit-compatible action definitions
- [ ] T029 [US3] Update `@cl.on_chat_start` in `src/vindicta_agents/ui/app.py` to render quick-action buttons from `get_playbook_actions()`
- [ ] T030 [US3] Add message handler in `src/vindicta_agents/ui/app.py` for quick-action button clicks that dispatches the selected workflow as intent
- [ ] T031 [US3] Run all User Story 3 tests and verify they pass

**Checkpoint**: Quick-action buttons are operational. Playbook workflows can be triggered with one click.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final verification, coverage, and documentation

- [ ] T032 [P] Run full test suite: `uv run pytest tests/ -v --cov=src/vindicta_agents --cov-report=term-missing`
- [ ] T033 [P] Run BDD tests: `uv run behave features/`
- [ ] T034 Run linting: `uv run ruff check src/vindicta_agents/ui/ src/vindicta_agents/swarm/nexus.py`
- [ ] T035 Run type checking: `uv run mypy src/vindicta_agents/ui/ src/vindicta_agents/swarm/nexus.py --strict`
- [ ] T036 Verify test coverage meets ≥90% threshold
- [ ] T037 Update `specs/010-chainlit-sqlite-persistence/quickstart.md` with final verified commands
- [ ] T038 Run quickstart.md validation end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Foundational phase — MVP target
- **US2 (Phase 4)**: Depends on Foundational phase — Can run parallel with US1 if desired
- **US3 (Phase 5)**: Depends on Foundational phase — Can run parallel with US1/US2
- **Polish (Phase 6)**: Depends on all user stories being complete

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Helper modules before app.py integration
- Core implementation before UI integration
- Story complete before moving to next priority

### Parallel Opportunities

- T001, T002, T003 (Setup) — all parallel
- T006, T007 (Foundational tests) — parallel
- T009, T010, T011 (US1 tests) — parallel
- T018, T019 (US2 tests) — parallel
- T025, T026 (US3 tests) — parallel
- T027 (US3 module) parallel with US1/US2 implementation

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test state persistence independently
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → SQLite persistence works (MVP!)
3. Add User Story 2 → Test independently → Daily threads operational
4. Add User Story 3 → Test independently → Quick actions visible
5. Each story adds value without breaking previous stories

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Total: 38 tasks (3 setup, 5 foundational, 9 US1, 7 US2, 7 US3, 7 polish)
