from pathlib import Path

from thinking_coach.llm import FakeLLMClient
from thinking_coach.models import Stage
from thinking_coach.persistence import SQLiteRepository
from thinking_coach.rule_engine import RuleEngine
from thinking_coach.runtime import RuntimeController


def test_rule_pipeline_keeps_required_order(tmp_path: Path) -> None:
    repository = SQLiteRepository(tmp_path / "coach.db")
    repository.initialize()
    conversation = repository.create_conversation()
    state = repository.get_workflow_state(conversation.id)

    result = RuleEngine().evaluate(state, {"core_question": "Should AI replace programmers?"}, "/advance")

    assert [decision.rule for decision in result.decisions] == list(RuleEngine.ORDER)
    assert result.final_decision.requires_confirmation is True
    assert result.final_decision.target_stage is Stage.BUILDING


def test_controller_requires_confirmation_before_stage_change(tmp_path: Path) -> None:
    repository = SQLiteRepository(tmp_path / "coach.db")
    repository.initialize()
    controller = RuntimeController(repository, FakeLLMClient())
    conversation_id = controller.create_conversation()
    repository.save_memory_state(conversation_id, {"core_question": "Should AI replace programmers?"})

    pending = controller.handle_turn(conversation_id, "/advance")

    assert pending.current_stage is Stage.DEFINITION
    assert pending.pending_action is not None
    assert repository.get_workflow_state(conversation_id).current_stage is Stage.DEFINITION

    confirmed = controller.handle_turn(conversation_id, "yes")

    assert confirmed.current_stage is Stage.BUILDING
    assert confirmed.pending_action is None
    assert any(row["event_type"] == "stage_changed" for row in repository.list_state_events(conversation_id))
