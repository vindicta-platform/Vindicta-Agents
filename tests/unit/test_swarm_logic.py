import pytest
from vindicta_agents.swarm.meta_graph import product_owner_node, architect_node, adl_node
from vindicta_agents.swarm.domain_graph import tech_priest_node, logos_historian_node, void_banker_node
from vindicta_agents.swarm.state import VindictaState

def test_product_owner_node():
    state = {"intent": "Test Intent"}
    result = product_owner_node(state)
    assert result["current_phase"] == "planning"
    assert "spec_content" in result
    assert "[MOCKED EXECUTION]" in result["spec_content"]

def test_architect_node():
    state = {"spec_content": "Test Spec"}
    result = architect_node(state)
    assert "plan_content" in result
    assert "[MOCKED EXECUTION]" in result["plan_content"]

def test_adl_node():
    state = {"plan_content": "Test Plan"}
    result = adl_node(state)
    assert result["current_phase"] == "review"
    assert "tasks" in result
    assert len(result["tasks"]) == 3
    assert result["tasks"][0]["target_realm"] == "vindicta-engine"

def test_domain_nodes_activation():
    state = {"tasks": []}
    
    tp_result = tech_priest_node(state)
    assert "TechPriest activated" in tp_result["execution_log"]
    
    lh_result = logos_historian_node(state)
    assert "LogosHistorian activated" in lh_result["execution_log"]
    
    vb_result = void_banker_node(state)
    assert "VoidBanker activated" in vb_result["execution_log"]
