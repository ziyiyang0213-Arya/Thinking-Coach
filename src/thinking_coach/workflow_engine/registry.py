"""Stage handlers expose behavior metadata only; they cannot change workflow state."""

from dataclasses import dataclass

from thinking_coach.models import Stage


@dataclass(frozen=True)
class WorkflowHandler:
    stage: Stage
    goal: str
    input_requirements: tuple[str, ...]
    completion_criteria: tuple[str, ...]

    def build_context(self, memory: dict[str, object]) -> str:
        return f"stage={self.stage}; goal={self.goal}; memory={memory}"


class WorkflowRegistry:
    def __init__(self) -> None:
        self._handlers = {
            Stage.DEFINITION: WorkflowHandler(Stage.DEFINITION, "Clarify the core question.", (), ("Core Question",)),
            Stage.BUILDING: WorkflowHandler(
                Stage.BUILDING, "Help the user structure their own position.", ("Core Question",), ("Position", "Reasoning")
            ),
        }

    def get(self, stage: Stage) -> WorkflowHandler:
        return self._handlers[stage]
