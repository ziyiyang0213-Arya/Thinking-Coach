from pathlib import Path

from thinking_coach.llm import ScriptedFakeLLMClient
from thinking_coach.models import LLMOutput, Stage
from thinking_coach.persistence import SQLiteRepository
from thinking_coach.runtime import RuntimeController


def facts(**values: object) -> list[dict[str, object]]:
    return [{"key": key, "value": value} for key, value in values.items()]


def advance(controller: RuntimeController, conversation_id: str) -> None:
    pending = controller.handle_turn(conversation_id, "/advance")
    assert pending.pending_action is not None
    controller.handle_turn(conversation_id, "yes")


def test_fake_llm_completes_a_full_thinking_session(tmp_path: Path) -> None:
    repository = SQLiteRepository(tmp_path / "coach.db")
    repository.initialize()
    llm = ScriptedFakeLLMClient(
        [
            LLMOutput(assistant_message="What is the question?", extracted_facts=facts(core_question="Will AI replace programmers?", original_thinking="AI will not fully replace programmers.")),
            LLMOutput(assistant_message="What is your position?", extracted_facts=facts(user_position="Jobs will change, not disappear.", basic_reasoning="Judgment remains necessary.", reasoning="Judgment remains necessary.", arguments=["Complex decisions require accountability."])),
            LLMOutput(assistant_message="Which assumption needs clarification?", extracted_facts=facts(refined_argument="Accountability matters in high-risk work.", assumptions=["Organizations value accountability."])),
            LLMOutput(assistant_message="How does your claim handle automation?", extracted_facts=facts(responses=["Automation may reduce entry roles."], debate_completed=True)),
            LLMOutput(assistant_message="State your conclusion.", extracted_facts=facts(current_thinking="AI may reduce some roles but not eliminate the profession.")),
            LLMOutput(assistant_message="What changed in your understanding?"),
        ]
    )
    controller = RuntimeController(repository, llm)
    conversation_id = controller.create_conversation()

    controller.handle_turn(conversation_id, "I want to think about AI and programmers.")
    advance(controller, conversation_id)
    controller.handle_turn(conversation_id, "My position is that jobs will change.")
    advance(controller, conversation_id)
    controller.handle_turn(conversation_id, "Please help me clarify it.")
    advance(controller, conversation_id)
    controller.handle_turn(conversation_id, "Start the debate.")
    advance(controller, conversation_id)
    controller.handle_turn(conversation_id, "I am ready to close.")
    advance(controller, conversation_id)
    reflection_turn = controller.handle_turn(conversation_id, "Reflect on what I expressed.")

    assert reflection_turn.current_stage is Stage.REFLECTION
    pending = controller.handle_turn(conversation_id, "/complete")
    assert pending.pending_action is not None
    completed = controller.handle_turn(conversation_id, "yes")

    assert "Reflection v1 saved" in completed.assistant_message
    assert len(repository.list_stage_snapshots(conversation_id)) == 6
    reflections = repository.list_reflections(conversation_id)
    assert len(reflections) == 1
    assert reflections[0].version == 1
    assert reflections[0].data["current_thinking"] == "AI may reduce some roles but not eliminate the profession."
