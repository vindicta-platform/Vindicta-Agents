# Architecture: Agent Domain Boundaries

The Vindicta ecosystem operates through two distinct categories of agents, each serving a specific purpose in the platform's lifecycle. Understanding the boundary between these domains is critical for both development and operational oversight.

## 1. Meta-Agents (The Development Swarm)

Meta-agents are the **builders**. Their primary responsibility is the construction, maintenance, and evolution of the Vindicta Platform itself.

- **Primary Domain**: The Codebase, GitHub Pipelines, and Development Process.
- **Roles**: Agile Delivery Lead (ADL), Architect, Senior Software Engineer (SSE), Product Owner, etc.
- **Governing Document**: The [Vindicta Agents Constitution](../.specify/memory/constitution.md).
- **Key Constraints**:
    - **Spec-Driven**: No implementation without an approved SDD bundle.
    - **Economic**: Must operate within the GCP Free Tier.
    - **Quality**: Mandated ≥90% test coverage and zero-issue stability.

## 2. Platform Agents (The Swarm Control Plane)

Platform agents are the **runtime governor**. They form the operational "nervous system" that manages active swarms of user-defined agents.

- **Primary Domain**: The Swarm Runtime and System State Management.
- **Key Components**:
    - **Nexus Orchestrator**: Coordinates inter-agent communication via WebSocket envelopes.
    - **Axiomatic Supervisor**: Validates all proposed state transitions.
- **Governing Document**: The [Zero-Order Axioms](../src/vindicta_agents/foundation/axioms.py).
- **Core Axioms**:
    - **AX-01**: Entity Identity (Unique, immutable UUIDs).
    - **AX-02**: Dimensionality (3D Euclidean space boundaries).
    - **AX-03**: Probability Source (Central Entropy Provider).
    - **AX-04**: Temporal Discretization (Discrete integer phases).

## Comparative Overview

| Feature             | Meta-Agents (Builders)                | Platform Agents (Runtime/Nexus)                 |
| :------------------ | :------------------------------------ | :---------------------------------------------- |
| **Logic Root**      | `agents/*`, `AGENT.md`, WORKFLOWS.md  | `nexus/orchestrator.py`, `foundation/axioms.py` |
| **Source of Truth** | Constitution (Process & Quality)      | Axioms (Physical & System Laws)                 |
| **Operating Space** | The project repository and CLI tools  | WebSocket envelopes and runtime state           |
| **Temporal Focus**  | Feature Lifecycle (Design → PR)       | State Lifecycle (Intent → Reality)              |
| **Communication**   | GitHub Issues/PRs, Markdown Artifacts | Standardized "Envelope" Protocol                |

## Domain Interaction

The Meta-Agents define the laws (Axioms) and build the infrastructure (Nexus) that the Platform Agents then enforce and manage at runtime. While Meta-Agents use MCP tools to manipulate the environment, Platform Agents use the Swarm Protocol to ensure the integrity of the active system.
