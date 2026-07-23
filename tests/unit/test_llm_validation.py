from pathlib import Path

from thinking_coach.llm import OutputValidator
from thinking_coach.models import LLMOutput, Stage
from thinking_coach.persistence import SQLiteRepository
from thinking_coach.runtime import RuntimeController


class UnsafeLLM:
    def generate(self, context: str) -> LLMOutput:
        return LLMOutput(
            assistant_message="I changed your stage.",
            proposed_actions=[{"action": "change_stage", "target": "debate"}],
        )


def test_validator_rejects_model_state_actions() -> None:
    output = LLMOutput(assistant_message="x", proposed_actions=[{"action": "topic_switch"}])
    try:
        OutputValidator().validate(output, Stage.DEFINITION)
    except ValueError as error:
        assert "reserved for the runtime" in str(error)
    else:
        raise AssertionError("Unsafe output must be rejected")


def test_rejected_llm_output_does_not_change_state_or_memory(tmp_path: Path) -> None:
    repository = SQLiteRepository(tmp_path / "coach.db")
    repository.initialize()
    controller = RuntimeController(repository, UnsafeLLM())
    conversation_id = controller.create_conversation()

    result = controller.handle_turn(conversation_id, "Change the stage")

    assert "rejected" in result.assistant_message
    assert result.current_stage is Stage.DEFINITION
    assert repository.get_memory_state(conversation_id) == {}
    assert repository.list_state_events(conversation_id) == []


def test_reflection_output_cannot_add_new_facts() -> None:
    output = LLMOutput(assistant_message="Reflection", extracted_facts=[{"key": "current_thinking", "value": "invented"}])
    try:
        OutputValidator().validate(output, Stage.REFLECTION)
    except ValueError as error:
        assert "cannot create new structured facts" in str(error)
    else:
        raise AssertionError("Reflection must not invent structured facts")
