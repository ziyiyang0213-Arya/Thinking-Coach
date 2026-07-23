"""State manager is the only service that commits approved workflow state changes."""

from thinking_coach.models import PendingAction, StageStatus, WorkflowState
from thinking_coach.persistence import SQLiteRepository


class StateManager:
    def __init__(self, repository: SQLiteRepository) -> None:
        self.repository = repository

    def set_pending(self, state: WorkflowState, action: PendingAction) -> WorkflowState:
        updated = state.model_copy(update={"stage_status": StageStatus.AWAITING_CONFIRMATION, "pending_action": action})
        self.repository.save_workflow_state(updated, "pending_action_created", action.model_dump(mode="json"))
        return updated

    def clear_pending(self, state: WorkflowState, event_type: str = "pending_action_cancelled") -> WorkflowState:
        updated = state.model_copy(update={"stage_status": StageStatus.ACTIVE, "pending_action": None})
        self.repository.save_workflow_state(updated, event_type, {})
        return updated

    def confirm_pending(self, state: WorkflowState) -> WorkflowState:
        action = state.pending_action
        if action is None or action.target_stage is None:
            raise ValueError("No confirmable state action exists.")
        updated = state.model_copy(
            update={"current_stage": action.target_stage, "stage_status": StageStatus.ACTIVE, "pending_action": None}
        )
        self.repository.save_workflow_state(
            updated,
            "stage_changed",
            {"action": action.action, "from": state.current_stage.value, "to": action.target_stage.value},
        )
        return updated
