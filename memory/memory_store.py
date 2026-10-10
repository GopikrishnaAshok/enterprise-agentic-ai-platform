import json
from pathlib import Path


MEMORY_FILE = Path(__file__).resolve().parent.parent / "data" / "memory.json"


def _load_memory() -> dict:
    """Load memory from local JSON storage."""

    if not MEMORY_FILE.exists():
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_memory(memory: dict) -> None:
    """Save memory to local JSON storage."""

    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=2, ensure_ascii=False)


def get_memory(user_id: str = "default") -> dict:
    """Retrieve stored memory for a user."""

    memory = _load_memory()

    return memory.get(user_id, {})


def save_memory(
    key: str,
    value: str,
    user_id: str = "default",
) -> None:
    """Save a memory item for a user."""

    memory = _load_memory()

    if user_id not in memory:
        memory[user_id] = {}

    memory[user_id][key] = value

    _save_memory(memory)


def clear_memory(user_id: str = "default") -> None:
    """Clear all stored memory for a user."""

    memory = _load_memory()

    if user_id in memory:
        del memory[user_id]

    _save_memory(memory)