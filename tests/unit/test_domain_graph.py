import sys
import unittest
from unittest.mock import patch, MagicMock
import os
import json

# Adjust path to import src
sys.path.append("src")

from vindicta_agents.swarm.domain_graph import build_domain_graph, run_integrity_check, make_domain_node, DOMAIN_REGISTRY

class TestDomainGraphStructure(unittest.TestCase):
    def test_graph_construction(self):
        """Verify that the graph is built with all registered domain nodes."""
        graph = build_domain_graph()
        
        # Access the underlying graph to check nodes
        # Note: CompiledStateGraph wraps the graph. We can check the nodes via get_graph()
        
        compiled_graph = graph.get_graph()
        nodes = compiled_graph.nodes
        
        # Check standard nodes
        self.assertIn("SetupExecution", nodes)
        
        # Check all registered domain nodes
        for realm, info in DOMAIN_REGISTRY.items():
            node_name = info["node_name"]
            self.assertIn(node_name, nodes, f"Node {node_name} for realm {realm} not found in graph")
            
class TestDomainGraphLogic(unittest.TestCase):
    
    @patch("vindicta_agents.swarm.domain_graph.subprocess.run")
    @patch("vindicta_agents.swarm.domain_graph._get_platform_root")
    @patch("os.path.isdir")
    def test_run_integrity_check_python(self, mock_isdir, mock_get_root, mock_run):
        """Test integrity check for a Python domain (vindicta-engine)."""
        mock_get_root.return_value = "/mock/platform/root"
        mock_isdir.return_value = True
        
        # Mock successful subprocess output
        expected_output = {"status": "ok", "details": "all systems nominal"}
        mock_run.return_value.stdout = json.dumps(expected_output)
        mock_run.return_value.returncode = 0
        
        result = run_integrity_check("vindicta-engine")
        
        self.assertEqual(result, expected_output)
        
        # Verify the command called
        args, kwargs = mock_run.call_args
        cmd = args[0]
        self.assertIn("uv", cmd)
        self.assertIn("python", cmd)
        self.assertIn("vindicta_engine", cmd[-1])
        
        # Check for cross-platform path compatibility
        expected_cwd = os.path.normpath(os.path.join("/mock/platform/root", "vindicta-engine"))
        self.assertEqual(os.path.normpath(kwargs["cwd"]), expected_cwd)

    @patch("vindicta_agents.swarm.domain_graph.subprocess.run")
    @patch("vindicta_agents.swarm.domain_graph._get_platform_root")
    @patch("os.path.isdir")
    def test_run_integrity_check_node_ui(self, mock_isdir, mock_get_root, mock_run):
        """Test integrity check for UI Kit (pnpm generic)."""
        mock_get_root.return_value = "/mock/platform/root"
        mock_isdir.return_value = True
        
        expected_output = {"status": "ok", "ui": "ready"}
        mock_run.return_value.stdout = json.dumps(expected_output)
        
        result = run_integrity_check("logi-slate-ui")
        self.assertEqual(result, expected_output)
        
        args, kwargs = mock_run.call_args
        cmd = args[0]
        self.assertEqual(cmd[0], "pnpm")
        self.assertIn("@vindicta/ui-kit", cmd)

    def test_make_domain_node_metadata(self):
        """Test that the generated node function has correct metadata."""
        node_func = make_domain_node("vindicta-engine")
        self.assertEqual(node_func.__name__, "techpriest_node")
        
    def test_missing_domain(self):
        """Test error handling for unknown domain."""
        result = run_integrity_check("non-existent-realm")
        self.assertEqual(result["status"], "error")
        self.assertIn("not found", result["error"])

if __name__ == "__main__":
    unittest.main()
