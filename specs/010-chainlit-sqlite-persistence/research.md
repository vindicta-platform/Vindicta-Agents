# Research: Chainlit SQLite Persistence

**Feature**: `010-chainlit-sqlite-persistence`
**Date**: 2026-02-12

## R1: LangGraph SQLite Checkpointer

**Decision**: Use `langgraph-checkpoint-sqlite` with `SqliteSaver`.

**Rationale**: Already declared as a dependency in `pyproject.toml` (`langgraph-checkpoint-sqlite>=3.0.3`). It provides a drop-in replacement for `MemorySaver` that implements the same `BaseCheckpointSaver` interface. Requires only a `sqlite3.Connection` object.

**Alternatives considered**:
- `langgraph-checkpoint-postgres` — Requires a running Postgres instance; violates the "local-only, zero-infrastructure" constraint.
- Custom file-based persistence — Unnecessary complexity when a battle-tested library already exists.
- Redis-backed persistence — Requires a Redis server; overkill for single-operator use.

## R2: Thread ID Strategy

**Decision**: Use date-keyed thread IDs in the format `daily-YYYY-MM-DD`.

**Rationale**: The Daily Playbook operates on a calendar-day cadence. A date-keyed thread ensures all workflows executed on the same day (SM check-in at 08:30, ADL PR review at 17:00) share the same state context. This aligns with the `config["configurable"]["thread_id"]` pattern used by LangGraph's `invoke()` method.

**Alternatives considered**:
- UUID per session (current behavior) — Breaks cross-workflow continuity; each session is isolated.
- Monotonically increasing counter — No semantic meaning; harder to query by date.
- Unix timestamp — Too granular; each invocation would create a new thread.

## R3: Checkpointer Injection Pattern

**Decision**: Modify `build_master_graph()` to accept an optional `checkpointer` parameter, defaulting to `MemorySaver()` for backward compatibility.

**Rationale**: This preserves all existing tests (which use the default `MemorySaver`) while allowing the Chainlit app and production paths to inject a `SqliteSaver`. The existing test file `test_nexus.py` imports `vindicta_swarm` directly, so the module-level `vindicta_swarm = build_master_graph()` must continue to use in-memory state.

**Alternatives considered**:
- Global singleton with SQLite — Would break all existing tests that expect ephemeral state.
- Environment variable toggle — More magical; harder to test deterministically.

## R4: Chainlit Quick Actions

**Decision**: Define playbook actions as a static list mapped from the Daily Playbook schedule, presented as `cl.Action` buttons in the chat interface.

**Rationale**: The Daily Playbook schedule (lines 10–22 of `daily-playbook.md`) is a known, fixed set of workflows. A static mapping is simpler and more reliable than dynamic discovery.

**Alternatives considered**:
- Parse `daily-playbook.md` at runtime — Fragile; file format changes would break the UI.
- Discover from `.agent/workflows/` directory listing — Over-engineered; most workflows are not part of the daily cadence.

## R5: Vault Directory Location

**Decision**: Store the SQLite database at `vault/swarm_state.sqlite` relative to the repo root.

**Rationale**: Follows the pattern of other Vindicta repos that use dedicated directories for runtime artifacts. The `vault/` name communicates "persistent, valuable data" in the Warhammer 40k theme. Added to `.gitignore` to prevent accidental commits.

**Alternatives considered**:
- `~/.vindicta/state.sqlite` (user home directory) — Decouples state from the repo; harder to reason about during development.
- `data/` directory — Too generic; could be confused with dataset/static-data directories.
