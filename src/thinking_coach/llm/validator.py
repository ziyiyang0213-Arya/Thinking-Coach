"""Validation boundary between model candidates and runtime-controlled state."""

from thinking_coach.models import LLMOutput, Stage


class OutputValidator:
    FORBIDDEN_ACTIONS = {
        "change_stage", "enter_stage", "topic_switch", "update_memory",
        "create_reflection", "complete_topic", "restart_cycle",
    }

    def validate(self, output: LLMOutput, stage: Stage) -> LLMOutput:
        if not output.assistant_message.strip():
            raise ValueError("assistant_message must not be empty")
        if stage is Stage.REFLECTION and output.extracted_facts:
            raise ValueError("Reflection output cannot create new structured facts")
        for action in output.proposed_actions:
            if action.get("action") in self.FORBIDDEN_ACTIONS:
                raise ValueError("LLM proposed an action reserved for the runtime")
        return output
