"""Planner integration tests; no Bedrock calls."""
import importlib

agent_module = importlib.import_module("backend.app.agents.agent")


def test_empty_request_skips_agent(monkeypatch):
    def forbidden(_prompt):
        raise AssertionError("Agent must not be called")
    monkeypatch.setattr(agent_module, "agent", forbidden)
    assert agent_module.ask_agent("   ") == "Request cannot be empty."


def test_document_roi_plan_is_included(monkeypatch):
    captured = []
    monkeypatch.setattr(agent_module, "agent", lambda prompt: captured.append(prompt) or "OK")
    monkeypatch.setattr(agent_module, "get_memory", lambda user_id: {})
    assert agent_module.ask_agent("According to the document, calculate ROI") == "OK"
    assert len(captured) == 1
    assert "document_analysis_and_calculation" in captured[0]
    assert "search_knowledge_base" in captured[0]
    assert "calculate_business_metrics" in captured[0]
    assert "Never invent values" in captured[0]


def test_general_request_uses_agent(monkeypatch):
    captured = []
    monkeypatch.setattr(agent_module, "agent", lambda prompt: captured.append(prompt) or "OK")
    monkeypatch.setattr(agent_module, "get_memory", lambda user_id: {})
    assert agent_module.ask_agent("Explain what an AI agent is") == "OK"
    assert len(captured) == 1
    assert "general_request" in captured[0]
    assert "agent_decides" in captured[0]


def test_memory_command_does_not_invoke_planner(monkeypatch):
    def forbidden(_prompt):
        raise AssertionError("Planner must not be called")
    monkeypatch.setattr(agent_module, "build_plan_context", forbidden)
    monkeypatch.setattr(agent_module, "get_memory", lambda user_id: {})
    assert agent_module.ask_agent("memory show") == "No saved memories found."
