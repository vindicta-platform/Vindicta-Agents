
from pydantic import BaseModel, Field, PrivateAttr
from typing import Optional, Any, Literal
import uuid
from uuid import UUID, uuid4

from ..telemetry.models import ResourceUsage
from ..governor.models import PriorityLevel

class ResourceRequirements(BaseModel):
    priority: PriorityLevel = PriorityLevel.NORMAL
    estimated_usage: ResourceUsage

class BaseAgent(BaseModel):
    """
    BaseAgent class responsible for the Handshake Protocol.
    """
    agent_id: str
    agent_class: str
    realm: str
    status: Literal["Offline", "Online", "Busy"] = "Offline"
    resources: Optional[ResourceRequirements] = None
    _websocket: Any = PrivateAttr(default=None)

    def handshake(self) -> bool:
        """
        Initiates the handshake with the Nexus (simulated).
        """
        # In a real implementation, this would communicate with the Nexus service.
        # For this stage, we verify self-consistency.
        if not self.realm:
            return False
        
        self.status = "Online"
        return True

    async def connect_to_nexus(self, nexus_url: str = "ws://localhost:8000/ws"):
        """
        Connects the agent to the Nexus Orchestrator via WebSocket.
        """
        try:
            import websockets
            uri = f"{nexus_url}/{self.agent_id}"
            self._websocket = await websockets.connect(uri)
            self.status = "Connected"
            print(f"[{self.agent_id}] Connected to Nexus at {uri}")
        except ImportError:
            print("websockets library not found. Install with: uv add websockets")
        except Exception as e:
            print(f"[{self.agent_id}] Failed to connect to Nexus: {e}")
            self.status = "Connection Failed"

    async def send_envelope(self, action: str, payload: dict) -> None:
        """
        Sends a WARScribeEnvelope to the Nexus.
        """
        if not self._websocket:
            print(f"[{self.agent_id}] Not connected to Nexus.")
            return

        envelope = {
            "trace_id": str(uuid.uuid4()),
            "sender": self.agent_id,
            "action": action,
            "payload": payload
        }
        
        try:
            import json
            await self._websocket.send(json.dumps(envelope))
            # Wait for ACK (simple implementation)
            response = await self._websocket.recv()
            print(f"[{self.agent_id}] Nexus ACK: {response}")
        except Exception as e:
             print(f"[{self.agent_id}] Error sending message: {e}")

    async def close(self):
        if self._websocket:
            await self._websocket.close()
            self.status = "Offline"
