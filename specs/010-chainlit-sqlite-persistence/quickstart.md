# Quickstart: Chainlit SQLite Persistence

**Feature**: `010-chainlit-sqlite-persistence`
**Date**: 2026-02-12

## Prerequisites

1. Python 3.12+ installed
2. `uv` package manager installed
3. Ollama installed and running (optional — MockLLMProvider used by default)

## Setup

```powershell
cd C:\Users\bfoxt\vindicta-platform\Vindicta-Agents
uv sync
```

## Launch the Chainlit UI

```powershell
uv run chainlit run src/vindicta_agents/ui/app.py -w
```

The `-w` flag enables hot-reload during development.

## Verify Persistence

### Test 1: State Survives Restart

1. Open the Chainlit UI in browser (usually `http://localhost:8000`)
2. Type an intent: `"Refactor the engine"`
3. Wait for planning to complete
4. Stop the server (Ctrl+C)
5. Restart the server with the same command
6. The previous session should be recoverable

### Test 2: Daily Thread Continuity

1. Open the Chainlit UI
2. Note the thread ID displayed (should be `daily-YYYY-MM-DD`)
3. Send a message: `"/sm-check-in"`
4. Close the browser tab
5. Reopen the UI — the same daily thread should be active

### Test 3: Quick Actions

1. Open the Chainlit UI
2. Verify quick-action buttons appear:
   - `/sm-check-in`
   - `/adl-standup`
   - `/adl-pr-review`
   - `/po-roadmap-update`
   - `/sm-end-day`
3. Click any button — it should invoke that workflow

## Run Tests

```powershell
# Unit tests
uv run pytest tests/unit/test_persistence.py -v

# All unit tests (verify nothing broken)
uv run pytest tests/unit/ -v --cov=src/vindicta_agents --cov-report=term-missing

# BDD tests
uv run behave features/persistence.feature
```

## Inspect the Database

```powershell
# View the SQLite database content
uv run python -c "import sqlite3; conn = sqlite3.connect('vault/swarm_state.sqlite'); print([t[0] for t in conn.execute('SELECT name FROM sqlite_master WHERE type=\"table\"').fetchall()])"
```
