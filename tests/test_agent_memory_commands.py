
import pytest

import memory.memory_store as memory_store
from backend.app.agents.agent import ask_agent


@pytest.fixture
def isolated_memory_file(tmp_path, monkeypatch):
    """Keep agent tests separate from real user memory."""
    test_file = tmp_path / "memory.json"
    monkeypatch.setattr(memory_store, "MEMORY_FILE", test_file)
    return test_file


def test_remember_command_saves_memory(isolated_memory_file):
    response = ask_agent(
        "remember: preferred_report_format = Executive summary",
        user_id="test_user",
    )

    assert "Memory saved successfully" in response
    assert memory_store.get_memory("test_user") == {
        "preferred_report_format": "Executive summary"
    }


def test_memory_show_displays_saved_values(isolated_memory_file):
    ask_agent(
        "remember: preferred_risk_count = 3",
        user_id="test_user",
    )

    response = ask_agent("memory show", user_id="test_user")

    assert "preferred_risk_count" in response
    assert "3" in response


def test_memory_clear_removes_selected_users_memory(isolated_memory_file):
    ask_agent(
        "remember: temporary_preference = test value",
        user_id="test_user",
    )

    response = ask_agent("memory clear", user_id="test_user")

    assert "cleared" in response.lower()
    assert memory_store.get_memory("test_user") == {}
