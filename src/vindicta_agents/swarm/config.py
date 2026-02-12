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

import json
import urllib.request
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


class OllamaLLMProvider:
    """
    Ollama implementation of LLMProvider protocol.
    Connects to local Ollama instance (default: http://localhost:11434).
    """
    def __init__(self, model: str = "llama3", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def execute(self, system: str | None, prompt: str) -> str:
        
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": f"System: {system}\nUser: {prompt}" if system else prompt,
            "stream": False
        }
        
        try:
            req = urllib.request.Request(
                url, 
                data=json.dumps(payload).encode('utf-8'), 
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get("response", "")
        except Exception as e:
            return f"[Ollama Error] {str(e)}"

    def execute_json(self, system: str | None, prompt: str) -> list[dict]:
        """Execute and parse JSON from the response, stripping markdown fences."""
        response = self.execute(system, prompt + "\nRespond ONLY with valid JSON.")
        try:
            clean = response.replace("```json", "").replace("```", "").strip()
            return json.loads(clean)
        except (json.JSONDecodeError, ValueError):
            return []


class SwarmConfig(TypedDict, total=False):
    """Configurable dependencies passed via RunnableConfig["configurable"]."""

    llm_provider: Any  # LLMProvider protocol
    supervisor: Any  # AxiomaticSupervisor instance
    nexus_client: Any  # Optional NexusClient for reporting
