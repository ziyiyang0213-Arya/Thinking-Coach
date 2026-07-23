from pathlib import Path

from thinking_coach.llm import FakeLLMClient, ScriptedFakeLLMClient
from thinking_coach.models import LLMOutput, Stage
from thinking_coach.persistence import SQLiteRepository
from thinking_coach.runtime import RuntimeController


def _facts(**values: object) -> list[dict[str, object]]:
    return [{"key": key, "value": value} for key, value in values.items()]


def _advance(controller: RuntimeController, conversation_id: str) -> None:
    assert controller.handle_turn(conversation_id, "/advance").pending_action
    controller.handle_turn(conversation_id, "yes")


def _cycle_outputs(label: str) -> list[LLMOutput]:
    return [
        LLMOutput(assistant_message="Define.", extracted_facts=_facts(core_question=f"Question {label}", original_thinking=f"Original {label}")),
        LLMOutput(assistant_message="Build.", extracted_facts=_facts(user_position=f"Position {label}", basic_reasoning="reason", reasoning="reason", arguments=["argument"])),
        LLMOutput(assistant_message="Refine.", extracted_facts=_facts(refined_argument="refined", assumptions=["assumption"])),
        LLMOutput(assistant_message="Debate.", extracted_facts=_facts(responses=["response"], debate_completed=True)),
        LLMOutput(assistant_message="Close.", extracted_facts=_facts(current_thinking=f"Current {label}")),
        LLMOutput(assistant_message="Reflect."),
    ]


def _run_cycle(controller: RuntimeController, conversation_id: str) -> None:
    controller.handle_turn(conversation_id, "definition")
    _advance(controller, conversation_id)
    controller.handle_turn(conversation_id, "building")
    _advance(controller, conversation_id)
    controller.handle_turn(conversation_id, "refinement")
    _advance(controller, conversation_id)
    controller.handle_turn(conversation_id, "debate")
    _advance(controller, conversation_id)
    controller.handle_turn(conversation_id, "closing")
    _advance(controller, conversation_id)
    controller.handle_turn(conversation_id, "reflection")


def test_topic_switch_creates_a_new_conversation_with_empty_memory(tmp_path: Path) -> None:
    repository = SQLiteRepository(tmp_path / "coach.db")
    repository.initialize()
    controller = RuntimeController(repository, FakeLLMClient())
    previous_id = controller.create_conversation()
    repository.save_memory_state(previous_id, {"core_question": "Old topic", "user_position": "Old position"})

    pending = controller.handle_turn(previous_id, "/topic Is remote work effective?")
    assert pending.pending_action is not None
    result = controller.handle_turn(previous_id, "yes")

    assert result.conversation_id != previous_id
    assert result.current_stage is Stage.DEFINITION
    assert repository.get_memory_state(result.conversation_id) == {}
    assert repository.get_conversation(previous_id).status.value == "closed"


def test_branching_is_confirmed_and_parked_in_structured_memory(tmp_path: Path) -> None:
    repository = SQLiteRepository(tmp_path / "coach.db")
    repository.initialize()
    controller = RuntimeController(repository, FakeLLMClient())
    conversation_id = controller.create_conversation()

    pending = controller.handle_turn(conversation_id, "/branch Compare hiring effects by seniority")
    assert pending.pending_action is not None
    confirmed = controller.handle_turn(conversation_id, "yes")

    assert confirmed.current_stage is Stage.DEFINITION
    assert repository.get_memory_state(conversation_id)["branches"] == [
        {"description": "Compare hiring effects by seniority", "status": "parked"}
    ]


def test_reflection_v2_requires_a_new_completed_cycle(tmp_path: Path) -> None:
    repository = SQLiteRepository(tmp_path / "coach.db")
    repository.initialize()
    controller = RuntimeController(repository, ScriptedFakeLLMClient(_cycle_outputs("one") + _cycle_outputs("two")))
    conversation_id = controller.create_conversation()

    _run_cycle(controller, conversation_id)
    assert controller.handle_turn(conversation_id, "/restart").pending_action
    restarted = controller.handle_turn(conversation_id, "yes")
    assert restarted.current_stage is Stage.DEFINITION
    assert restarted.pending_action is None
    assert len(repository.list_reflections(conversation_id)) == 1

    _run_cycle(controller, conversation_id)
    assert controller.handle_turn(conversation_id, "/complete").pending_action
    controller.handle_turn(conversation_id, "yes")

    reflections = repository.list_reflections(conversation_id)
    assert [record.version for record in reflections] == [1, 2]
    assert reflections[1].cycle_number == 2
