"""Stage handlers expose behavior metadata only; they cannot change workflow state."""

from dataclasses import dataclass

from thinking_coach.models import Stage


@dataclass(frozen=True)
class WorkflowHandler:
    stage: Stage
    goal: str
    input_requirements: tuple[str, ...]
    completion_criteria: tuple[str, ...]
    output_schema: tuple[str, ...]
    restrictions: tuple[str, ...]

    def build_context(self, memory: dict[str, object]) -> str:
        return f"stage={self.stage}; goal={self.goal}; memory={memory}"


class WorkflowRegistry:
    def __init__(self) -> None:
        self._handlers = {
            Stage.DEFINITION: WorkflowHandler(Stage.DEFINITION, "Clarify the core question.", (), ("Core Question",), ("assistant_message", "extracted_facts"), ("Do not answer the complex question for the user.",)),
            Stage.BUILDING: WorkflowHandler(Stage.BUILDING, "Help the user structure their own position.", ("Core Question",), ("Position", "Reasoning"), ("assistant_message", "extracted_facts"), ("Do not create the user's position.",)),
            Stage.REFINEMENT: WorkflowHandler(Stage.REFINEMENT, "Collaboratively clarify and strengthen the user's argument.", ("Position", "Reasoning"), ("Refined Argument",), ("assistant_message", "extracted_facts"), ("Do not adopt an opponent role.",)),
            Stage.DEBATE: WorkflowHandler(Stage.DEBATE, "Pressure-test the user's actual claim as an opponent.", ("Position", "Reasoning", "Argument"), ("Challenges and responses",), ("assistant_message", "extracted_facts"), ("Do not supply missing arguments for the user.",)),
            Stage.CLOSING: WorkflowHandler(Stage.CLOSING, "Help the user express their own closing statement.", ("Completed Debate",), ("Current Thinking",), ("assistant_message", "extracted_facts"), ("Do not write the user's closing statement.",)),
            Stage.REFLECTION: WorkflowHandler(Stage.REFLECTION, "Record the user's expressed cognitive state.", ("Original Thinking", "Current Thinking"), ("Reflection Record",), ("assistant_message", "extracted_facts"), ("Do not add unexpressed insights or evaluate growth.",)),
        }

    def get(self, stage: Stage) -> WorkflowHandler:
        return self._handlers[stage]
