from pathlib import Path

from thinking_coach.llm import FakeLLMClient
from thinking_coach.models import Stage
from thinking_coach.persistence import SQLiteRepository
from thinking_coach.runtime import RuntimeController


def test_runtime_persists_messages_without_changing_stage(tmp_path: Path) -> None:
    repository = SQLiteRepository(tmp_path / "coach.db")
    repository.initialize()
    controller = RuntimeController(repository, FakeLLMClient())
    conversation_id = controller.create_conversation()

    result = controller.handle_turn(conversation_id, "我想思考 AI 是否会取代程序员。")

    assert result.current_stage is Stage.DEFINITION
    assert len(repository.list_messages(conversation_id)) == 2
    assert repository.get_workflow_state(conversation_id).current_stage is Stage.DEFINITION
