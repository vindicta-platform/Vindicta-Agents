"""
Swarm Configuration & Dependency Injection
===========================================
Defines the configurable dependencies injected into LangGraph nodes
via RunnableConfig["configurable"].

Usage:
    vindicta_swarm.invoke(state, config={"configurable": {
        "llm_provider": my_provider,
        "supervisor": my_supervisor,
    }})
"""

from typing import Any, Protocol, TypedDict, runtime_checkable


@runtime_checkable
class LLMProvider(Protocol):
    """Protocol for LLM execution backends."""

    def execute(self, system: str | None, prompt: str) -> str: ...

    def execute_json(self, system: str | None, prompt: str) -> list[dict]: ...


class MockLLMProvider:
    """Default mock implementation for development and testing."""

    def execute(self, system: str | None, prompt: str) -> str:
        return f"[MOCKED EXECUTION] System: {system} | User: {prompt}"

    def execute_json(self, system: str | None, prompt: str) -> list[dict]:
        return [
            {
                "id": "task-1",
                "description": "Implement core engine logic",
                "target_realm": "vindicta-engine",
                "status": "pending",
            },
            {
                "id": "task-2",
                "description": "Implement warscribe parsing",
                "target_realm": "warscribe-system",
                "status": "pending",
            },
            {
                "id": "task-3",
                "description": "Implement economy features",
                "target_realm": "vindicta-economy",
                "status": "pending",
            },
        ]


class SwarmConfig(TypedDict, total=False):
    """Configurable dependencies passed via RunnableConfig["configurable"]."""

    llm_provider: Any  # LLMProvider protocol
    supervisor: Any  # AxiomaticSupervisor instance
    nexus_client: Any  # Optional NexusClient for reporting
