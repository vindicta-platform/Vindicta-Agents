import sys
import unittest
from unittest.mock import MagicMock

# Adjust path to import src
sys.path.append("src")

from vindicta_agents.swarm.meta_graph import build_meta_graph, make_planning_node, PLANNING_AGENTS
from vindicta_agents.swarm.state import VindictaState

class TestMetaGraphRefactor(unittest.TestCase):
    
    def test_graph_structure(self):
        """Verify the meta graph contains all planning nodes."""
        graph = build_meta_graph()
        compiled_graph = graph.get_graph()
        nodes = compiled_graph.nodes
        
        self.assertIn("PO", nodes)
        self.assertIn("Architect", nodes)
        self.assertIn("ADL", nodes)
        
    def test_po_node_execution(self):
        """Test the PO node logic (generic simple text execution)."""
        po_node = make_planning_node("PO")
        
        state: VindictaState = {"intent": "Build a death star", "tasks": [], "execution_log": []} # type: ignore
        config = {"configurable": {}}
        
        # Test with default MockLLMProvider
        result = po_node(state, config)
        
        self.assertIn("spec_content", result)
        self.assertIn("[MOCKED EXECUTION]", result["spec_content"])
        self.assertEqual(result["current_phase"], "planning")
        
    def test_adl_node_execution(self):
        """Test the ADL node logic (generic JSON execution)."""
        adl_node = make_planning_node("ADL")
        
        state: VindictaState = {"plan_content": "Execute order 66", "tasks": [], "execution_log": []} # type: ignore
        config = {"configurable": {}}
        
        result = adl_node(state, config)
        
        self.assertIn("tasks", result)
        self.assertIsInstance(result["tasks"], list)
        self.assertEqual(result["current_phase"], "review")
        # specific check for mock data
        self.assertEqual(result["tasks"][0]["target_realm"], "vindicta-engine")

if __name__ == "__main__":
    unittest.main()
