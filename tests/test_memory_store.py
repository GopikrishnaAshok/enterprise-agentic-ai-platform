
import json

import pytest

import memory.memory_store as memory_store


@pytest.fixture
def isolated_memory_file(tmp_path, monkeypatch):
    """Use a temporary JSON file so real user memory is untouched."""
    test_file = tmp_path / "memory.json"
    monkeypatch.setattr(memory_store, "MEMORY_FILE", test_file)
    return test_file


def test_save_and_retrieve_memory(isolated_memory_file):
    memory_store.save_memory(
        "preferred_report_format",
        "Executive summary",
    )

    result = memory_store.get_memory()

    assert result == {
        "preferred_report_format": "Executive summary",
    }


def test_update_existing_memory(isolated_memory_file):
    memory_store.save_memory("preferred_risk_count", "3")
    memory_store.save_memory("preferred_risk_count", "5")

    result = memory_store.get_memory()

    assert result["preferred_risk_count"] == "5"
    assert len(result) == 1


def test_memories_persist_in_json_file(isolated_memory_file):
    memory_store.save_memory("language", "English")

    with open(isolated_memory_file, "r", encoding="utf-8") as file:
        saved_data = json.load(file)

    assert saved_data["default"]["language"] == "English"


def test_memory_is_isolated_by_user(isolated_memory_file):
    memory_store.save_memory(
        "preferred_report_format",
        "Executive summary",
        user_id="user_a",
    )
    memory_store.save_memory(
        "preferred_report_format",
        "Detailed report",
        user_id="user_b",
    )

    assert memory_store.get_memory("user_a") == {
        "preferred_report_format": "Executive summary",
    }
    assert memory_store.get_memory("user_b") == {
        "preferred_report_format": "Detailed report",
    }


def test_clear_memory_removes_only_selected_user(isolated_memory_file):
    memory_store.save_memory("theme", "dark", user_id="user_a")
    memory_store.save_memory("theme", "light", user_id="user_b")

    memory_store.clear_memory("user_a")

    assert memory_store.get_memory("user_a") == {}
    assert memory_store.get_memory("user_b") == {"theme": "light"}


def test_missing_memory_file_returns_empty_dictionary(
    isolated_memory_file,
):
    assert not isolated_memory_file.exists()
    assert memory_store.get_memory() == {}


def test_corrupt_json_returns_empty_dictionary(isolated_memory_file):
    isolated_memory_file.write_text("{invalid json", encoding="utf-8")

    assert memory_store.get_memory() == {}
