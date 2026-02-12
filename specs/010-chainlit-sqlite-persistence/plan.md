# Implementation Plan: Chainlit UI with SQLite Persistence

**Branch**: `010-chainlit-sqlite-persistence` | **Date**: 2026-02-12 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/010-chainlit-sqlite-persistence/spec.md`

## Summary

Upgrade the Vindicta Swarm's Chainlit UI from ephemeral in-memory state (`MemorySaver`) to persistent SQLite-backed state (`SqliteSaver`), enabling cross-session continuity for the Daily Playbook workflow on a local Windows machine. The changes involve refactoring `nexus.py` to accept an injectable checkpointer, updating `ui/app.py` to use date-keyed daily threads and playbook quick-actions, and adding a `vault/` directory for the SQLite database.

## Technical Context

**Language/Version**: Python 3.12
**Primary Dependencies**: langgraph, langgraph-checkpoint-sqlite (already in pyproject.toml), chainlit >=1.0.0 (already in pyproject.toml), structlog
**Storage**: SQLite via `langgraph-checkpoint-sqlite` at `vault/swarm_state.sqlite`
**Testing**: pytest (unit), behave (BDD)
**Target Platform**: Windows 10/11 local machine
**Project Type**: Single project
**Performance Goals**: <200ms checkpoint write, <50MB database after 30 daily cycles
**Constraints**: Must run offline (no cloud dependencies), must not break existing tests
**Scale/Scope**: Single operator, 1–10 daily workflow invocations

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle                           | Status | Notes                                      |
| ----------------------------------- | ------ | ------------------------------------------ |
| I. MCP-First Mandate                | ✅ PASS | No GitHub/GCP/Firebase operations involved |
| II. Spec-Driven Development         | ✅ PASS | Full SDD bundle being created              |
| III. Economic Prime Directive       | ✅ PASS | SQLite is free, runs locally               |
| IV. Zero-Issue Stability            | ✅ PASS | No existing issues introduced              |
| V. Vanilla-Forward & Modern Tooling | ✅ PASS | Python stdlib + established libraries      |
| VI. Axiom-Driven Design             | ✅ PASS | State uses existing `VindictaState` schema |
| VII. Agent-First Architecture       | ✅ PASS | Enhances agent orchestration capabilities  |
| QG-1 Linting & Formatting           | ✅ PASS | All code must pass ruff + mypy --strict    |
| QG-2 Test Coverage ≥90%             | ✅ PASS | Tests planned for all new code             |
| QG-3 Link Integrity                 | ✅ PASS | No documentation links modified            |
| QG-4 Agent Context                  | ✅ PASS | No .antigravity artifacts affected         |

## Project Structure

### Documentation (this feature)

```text
specs/010-chainlit-sqlite-persistence/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── tasks.md             # Phase 2 output
└── checklists/
    └── requirements.md  # Spec quality validation
```

### Source Code (repository root)

```text
src/vindicta_agents/
├── swarm/
│   └── nexus.py              # MODIFY: Injectable checkpointer
├── ui/
│   ├── app.py                # MODIFY: SQLite + daily threads + quick-actions
│   └── playbook_actions.py   # NEW: Quick-action definitions
vault/                         # NEW: Persistent storage (gitignored)
└── swarm_state.sqlite         # Auto-created at runtime

tests/
├── unit/
│   ├── test_nexus.py          # EXISTS: Update for checkpointer injection
│   └── test_persistence.py    # NEW: SQLite persistence tests
└── (existing tests unmodified)

features/
├── swarm.feature              # EXISTS: Verify still passes
└── persistence.feature        # NEW: BDD for persistence scenarios
```

**Structure Decision**: Single project layout. The `vault/` directory is created at repo root for persistent storage, gitignored. All source changes are within the existing `src/vindicta_agents/` tree.

## Complexity Tracking

> No constitution violations. No complexity justification needed.
