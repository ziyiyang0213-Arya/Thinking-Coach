from pathlib import Path

from thinking_coach.llm import FakeLLMClient
from thinking_coach.persistence import SQLiteRepository
from thinking_coach.runtime import RuntimeController


def test_conversation_history_is_not_copied_into_structured_memory(tmp_path: Path) -> None:
    repository = SQLiteRepository(tmp_path / "coach.db")
    repository.initialize()
    controller = RuntimeController(repository, FakeLLMClient())
    conversation_id = controller.create_conversation()

    controller.handle_turn(conversation_id, "This raw sentence belongs only to history.")

    assert len(repository.list_messages(conversation_id)) == 2
    assert repository.get_memory_state(conversation_id) == {}
