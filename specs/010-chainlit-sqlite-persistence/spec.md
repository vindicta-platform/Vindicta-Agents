# Feature Specification: Chainlit UI with SQLite Persistence

**Feature Branch**: `010-chainlit-sqlite-persistence`
**Created**: 2026-02-12
**Status**: Draft
**Input**: User description: "Plan the Chainlit setup with persistence into SQLite using Python — automating the Daily Playbook workflow locally on Windows."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Persistent Swarm Memory (Priority: P1)

As a Platform Operator, I want the swarm's execution state to survive process restarts so that the morning check-in context (08:30) is still available when the evening PR review runs (17:00), even if the process was restarted in between.

**Why this priority**: Without persistence, every workflow invocation starts from scratch. The entire Daily Playbook model depends on state continuity across a full workday. This is the foundational prerequisite for all other stories.

**Independent Test**: Can be tested by invoking the swarm with an intent, stopping the process, restarting it, and verifying that the previous state (tasks, phase, execution log) is fully recoverable from the SQLite database.

**Acceptance Scenarios**:

1. **Given** a swarm session with completed planning tasks, **When** the process is stopped and restarted, **Then** the previous session's state (intent, tasks, phase, execution log) is fully recoverable.
2. **Given** multiple daily sessions stored in the database, **When** a user queries for a specific date's thread, **Then** the system returns the correct session state without data leakage between threads.
3. **Given** a corrupt or missing database file, **When** the system starts, **Then** it creates a fresh database and logs a warning without crashing.

---

### User Story 2 - Daily Thread Management (Priority: P1)

As a Platform Operator, I want the system to automatically create a date-keyed thread each day so that all playbook workflows executed on the same day share context, and I can review any past day's activity.

**Why this priority**: The Daily Playbook schedule requires multiple agents (SM, ADL, PO) to share state within a single day. Date-based threading is the mechanism that enables this coordination.

**Independent Test**: Can be tested by verifying that two messages sent on the same day use the same thread ID, and messages sent on different days use different thread IDs.

**Acceptance Scenarios**:

1. **Given** a new calendar day, **When** the Chainlit app starts a session, **Then** a thread ID matching the format `daily-YYYY-MM-DD` is created.
2. **Given** an existing thread for today, **When** a second workflow is invoked, **Then** it appends to the same daily thread instead of creating a new one.
3. **Given** it is a new day, **When** the operator opens the interface, **Then** a fresh daily thread is created while past threads remain accessible.

---

### User Story 3 - Playbook Quick Actions (Priority: P2)

As a Platform Operator, I want the Chainlit interface to provide quick-action buttons for each playbook workflow so that I can trigger the daily rhythm with a single click instead of typing commands manually.

**Why this priority**: Reduces friction for daily operations. The operator should not need to memorize slash commands — the interface should present the current schedule context-aware actions.

**Independent Test**: Can be tested by launching the Chainlit UI and verifying that quick-action buttons appear for relevant playbook workflows and that clicking one correctly invokes the swarm with the appropriate intent.

**Acceptance Scenarios**:

1. **Given** the Chainlit app starts, **When** the operator views the interface, **Then** quick-action buttons for the current time-window's playbook workflows are visible.
2. **Given** the operator clicks the "/sm-check-in" quick action, **When** the swarm processes it, **Then** the intent is set to the SM check-in workflow and execution begins.
3. **Given** a workflow completes, **When** the next workflow's time window arrives, **Then** updated quick-action buttons reflect the new context.

---

### Edge Cases

- What happens when the SQLite database file is locked by another process?
- How does the system handle a thread ID collision (e.g., clock rollback)?
- What happens if the Chainlit UI is opened in multiple browser tabs simultaneously?
- How does the system behave when disk space is exhausted and SQLite cannot write?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST persist all swarm state to a local SQLite database at `vault/swarm_state.sqlite`.
- **FR-002**: System MUST use date-keyed thread IDs (`daily-YYYY-MM-DD`) for all Daily Playbook sessions.
- **FR-003**: System MUST allow recovery of any previous day's session state by thread ID.
- **FR-004**: System MUST provide quick-action buttons in the Chainlit interface for playbook workflows.
- **FR-005**: System MUST gracefully handle database creation on first run (auto-initialize schema).
- **FR-006**: System MUST fall back to in-memory state if the SQLite connection fails, logging a warning.
- **FR-007**: System MUST support the existing Human-in-the-Loop review flow (approve/reject) with persistent state.
- **FR-008**: The `vault/` directory MUST be excluded from version control via `.gitignore`.

### Key Entities

- **DailyThread**: Represents a single day's swarm session. Key attributes: thread ID (date-keyed), creation timestamp, associated VindictaState snapshots.
- **SwarmCheckpoint**: A LangGraph-managed state snapshot. Key attributes: thread ID, checkpoint ID, serialized state, timestamp.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Swarm state survives a full process restart cycle (stop → start) with zero data loss, verified by comparing pre-restart and post-restart state snapshots.
- **SC-002**: The system operates correctly across a simulated full-day playbook cycle (morning check-in through evening close-out) using a single persistent daily thread.
- **SC-003**: All existing unit and BDD tests continue to pass with the persistence layer enabled.
- **SC-004**: Quick-action buttons for at least 5 core playbook workflows are accessible within one click from the main interface.
- **SC-005**: Database file size remains under 50 MB after 30 simulated daily cycles.
