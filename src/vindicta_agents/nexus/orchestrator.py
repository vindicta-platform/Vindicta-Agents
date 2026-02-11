from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field
from typing import Dict, Any, List
import uuid
import asyncio
import uvicorn
import json

# Data Models
class WARScribeEnvelope(BaseModel):
    """
    Standard Envelope for all Swarm Communication.
    """
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sender: str
    receiver: str = "Nexus"
    action: str
    payload: Dict[str, Any]

class AgentRegistry:
    """
    Tracks active agents and their WebSocket connections.
    """
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, agent_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[agent_id] = websocket
        print(f"[NEXUS] Agent Connected: {agent_id}")

    def disconnect(self, agent_id: str):
        if agent_id in self.active_connections:
            del self.active_connections[agent_id]
            print(f"[NEXUS] Agent Disconnected: {agent_id}")

    async def send_personal_message(self, message: str, agent_id: str):
        if agent_id in self.active_connections:
            await self.active_connections[agent_id].send_text(message)

from ..telemetry.monitor import HardwareMonitor
from ..governor.resource_manager import ResourceGovernor
from ..governor.models import PriorityLevel

# Nexus Application
app = FastAPI()
registry = AgentRegistry()

# Initialize Telemetry & Governor
monitor = HardwareMonitor()
governor = ResourceGovernor(monitor)

@app.on_event("startup")
async def startup_event():
    monitor.start()
    print("[NEXUS] Hardware Monitor Started")

@app.on_event("shutdown")
async def shutdown_event():
    monitor.stop()
    print("[NEXUS] Hardware Monitor Stopped")

@app.websocket("/ws/{agent_id}")
async def websocket_endpoint(websocket: WebSocket, agent_id: str):
    # 1. Resource Check (Handshake Phase)
    decision = governor.check_resources(PriorityLevel.NORMAL) # Default priority
    if decision.should_throttle:
        await websocket.accept()
        await websocket.send_text(json.dumps({
            "error": "THROTTLED",
            "reason": decision.reason,
            "wait_time": decision.suggested_wait_time
        }))
        await websocket.close()
        return

    await registry.connect(agent_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # 1. Parse Envelope
            try:
                envelope_dict = json.loads(data)
                envelope = WARScribeEnvelope(**envelope_dict)
                
                # 2. Process Message (Stub for Supervisor integration)
                print(f"[NEXUS] Received from {agent_id}: {envelope.action}")
                
                # Echo back for confirmation (Temporary)
                response = {
                    "trace_id": envelope.trace_id,
                    "sender": "Nexus",
                    "receiver": agent_id,
                    "action": "ACK",
                    "payload": {"status": "Received"}
                }
                await registry.send_personal_message(json.dumps(response), agent_id)
                
            except Exception as e:
                print(f"[NEXUS] Error processing message: {e}")
                error_response = {"error": str(e)}
                await registry.send_personal_message(json.dumps(error_response), agent_id)

    except WebSocketDisconnect:
        registry.disconnect(agent_id)

def start_nexus(host: str = "0.0.0.0", port: int = 8000):
    """
    Starts the Nexus Orchestrator.
    """
    uvicorn.run(app, host=host, port=port)
