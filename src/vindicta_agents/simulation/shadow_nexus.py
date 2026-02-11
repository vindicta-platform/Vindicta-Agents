import asyncio
import uuid
import json
from typing import Dict, Any, List
from vindicta_agents.supervisor.gatekeeper import AxiomaticSupervisor, AxiomApproval, ConstitutionalHalt
from vindicta_agents.shared.memory import SharedMemory
from vindicta_agents.simulation.scenarios import Scenario, ScenarioAction
from vindicta_agents.utils.logger import FlightRecorder

class ShadowNexus:
    """
    Simulated Nexus Orchestrator for Shadow Mode.
    Executes predefined scenarios to validate Supervisor logic.
    """
    def __init__(self):
        self.supervisor = AxiomaticSupervisor()
        self.memory = SharedMemory()
        self.recorder = FlightRecorder() # Access existing DB or create new test DB?
        # For simulation, we might want a separate DB or just use the main one with specific trace_ids.
        # Supervisor already has a reference to recorder.

    def load_scenario(self, scenario: Scenario):
        """
        Resets state and loads the scenario.
        """
        print(f"[SHADOW] Loading Scenario: {scenario.name}")
        self.memory.reset()
        if scenario.initial_state_delta:
            self.memory.state.update(scenario.initial_state_delta)
        print(f"[SHADOW] Initial State: {self.memory.state}")

    async def run_scenario(self, scenario: Scenario) -> Dict[str, Any]:
        """
        Executes actions in the scenario and verifies outcomes.
        Returns a report of pass/fail.
        """
        self.load_scenario(scenario)
        results = {
            "scenario": scenario.name,
            "passed": True,
            "steps": []
        }

        for action in scenario.actions:
            trace_id = str(uuid.uuid4())
            print(f"[SHADOW] Tick {action.tick}: Agent {action.agent_id} attempting {action.action_type}...")
            
            # 1. Propose State Transition (Simulated Agent Action)
            # In real Nexus, this comes via WebSocket. Here, we call Supervisor directly.
            
            outcome = self.supervisor.verify_state_transition(
                trace_id=trace_id,
                proposed_delta=action.payload
            )
            
            # 2. Verify Outcome
            actual_type = "AXIOM_APPROVAL" if isinstance(outcome, AxiomApproval) else "CONSTITUTIONAL_HALT"
            match = actual_type == action.expected_outcome
            
            step_result = {
                "tick": action.tick,
                "agent": action.agent_id,
                "expected": action.expected_outcome,
                "actual": actual_type,
                "match": match,
                "trace_id": trace_id
            }
            results["steps"].append(step_result)
            
            if not match:
                results["passed"] = False
                print(f"  [FAIL] Expected {action.expected_outcome}, got {actual_type}")
            else:
                print(f"  [PASS] {actual_type} confirmed.")
                
        return results
