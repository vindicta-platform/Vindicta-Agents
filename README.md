> **Part of the [Vindicta Platform](https://github.com/vindicta-platform)**

# Vindicta Agents

SDKs, Workflows, and Swarm for the Vindicta Platform.

## Installation

```bash
uv sync
```

## Features

- **Agent SDK**: Base classes and protocol for Vindicta Agents.
- **Swarm Management**: Coordination and orchestration logic.
- **Auditor Integration**: Rate limiting and quota auditing.

## Testing & Coverage

```bash
uv run pytest --cov
uv run behave
```
Coverage Mandate: ≥90%

## Docs

- [SDK Reference](docs/sdk.md)
- [Workflow Guide](docs/index.md)
