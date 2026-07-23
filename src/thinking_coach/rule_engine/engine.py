"""Rule pipeline. Rule evaluators return decisions; they never persist state."""

from dataclasses import dataclass

from thinking_coach.models import RuleDecision, Stage, WorkflowState
from thinking_coach.state.machine import can_enter, next_stage


@dataclass(frozen=True)
class PipelineResult:
    decisions: list[RuleDecision]

    @property
    def final_decision(self) -> RuleDecision:
        return next((decision for decision in self.decisions if decision.action != "none"), self.decisions[-1])


class RuleEngine:
    ORDER = ("topic_change", "viewpoint_change", "stage_transition", "memory_update")

    def evaluate(
        self, workflow_state: WorkflowState, memory: dict[str, object], user_input: str
    ) -> PipelineResult:
        decisions = [
            RuleDecision(rule="topic_change"),
            RuleDecision(rule="viewpoint_change"),
            self._stage_transition(workflow_state, memory, user_input),
            RuleDecision(rule="memory_update", memory_effects=["current_state_candidate"]),
        ]
        return PipelineResult(decisions)

    def _stage_transition(
        self, state: WorkflowState, memory: dict[str, object], user_input: str
    ) -> RuleDecision:
        command = user_input.strip().lower()
        target: Stage | None = None
        action = "advance"
        if command == "/advance":
            target = next_stage(state.current_stage)
        elif command == "/complete" and state.current_stage is Stage.REFLECTION:
            return RuleDecision(
                rule="stage_transition", action="complete_reflection", reason="Request to finalize the current Reflection.",
                requires_confirmation=True,
            )
        elif command == "/rollback":
            target = Stage.REFINEMENT
            action = "rollback"
        elif command.startswith("/skip "):
            try:
                target = Stage(command.removeprefix("/skip ").strip())
            except ValueError:
                return RuleDecision(rule="stage_transition", action="deny", reason="Unknown skip target.")
            action = "skip"
        else:
            return RuleDecision(rule="stage_transition")

        if target is None:
            return RuleDecision(rule="stage_transition", action="deny", reason="No later stage exists.")
        allowed, missing = can_enter(state.current_stage, target, memory)
        if not allowed:
            return RuleDecision(
                rule="stage_transition", action="deny", reason="Target stage requirements are not satisfied.", required_inputs=missing
            )
        return RuleDecision(
            rule="stage_transition", action=action, reason=f"Request to enter {target.value}.",
            requires_confirmation=True, target_stage=target,
        )
