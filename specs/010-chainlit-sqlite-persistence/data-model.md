# Data Model: Chainlit SQLite Persistence

**Feature**: `010-chainlit-sqlite-persistence`
**Date**: 2026-02-12

## Entities

### VindictaState (Existing — No Changes)

The canonical state schema shared by all sub-graphs in the Vindicta Swarm. Defined in `src/vindicta_agents/swarm/state.py`.

| Field         | Type          | Description                                             |
| ------------- | ------------- | ------------------------------------------------------- |
| intent        | str           | User's input goal/request                               |
| spec_content  | Optional[str] | Generated specification from PO agent                   |
| plan_content  | Optional[str] | Generated plan from Architect agent                     |
| tasks         | List[Task]    | Accumulated tasks (reducer: `operator.add`)             |
| current_phase | str           | `planning` / `review` / `execution` / `done`            |
| error_log     | Optional[str] | Error details if any                                    |
| execution_log | List[str]     | Accumulated execution entries (reducer: `operator.add`) |

### Task (Existing — No Changes)

| Field        | Type          | Description                                        |
| ------------ | ------------- | -------------------------------------------------- |
| id           | str           | Unique task identifier                             |
| description  | str           | Human-readable task description                    |
| target_realm | str           | Target repository key                              |
| status       | str           | `pending` / `in-progress` / `completed` / `failed` |
| code_diff    | Optional[str] | Generated code changes                             |

### SwarmCheckpoint (Managed by LangGraph — No Custom Schema)

LangGraph's `SqliteSaver` manages its own schema internally. The checkpoint table stores:

| Column        | Type | Description                                  |
| ------------- | ---- | -------------------------------------------- |
| thread_id     | TEXT | Thread identifier (e.g., `daily-2026-02-12`) |
| checkpoint_id | TEXT | Unique checkpoint within a thread            |
| parent_id     | TEXT | Parent checkpoint (for branching)            |
| checkpoint    | BLOB | Serialized graph state                       |
| metadata      | BLOB | Serialized metadata                          |

> **Note**: No custom migrations or schema modifications are needed. `SqliteSaver` auto-creates its tables on first use.

## Relationships

```
DailyThread (thread_id: "daily-YYYY-MM-DD")
    └── has many → SwarmCheckpoints
        └── each contains → serialized VindictaState
            ├── tasks[]
            ├── execution_log[]
            └── spec_content / plan_content
```

## State Transitions

```
VindictaState.current_phase:
  "planning" → "review" → "execution" → "done"
                  ↑                        │
                  └──── (reject) ──────────┘
```
