"""State manager is the only service that commits approved workflow state changes."""

from thinking_coach.models import ConversationStatus, PendingAction, Stage, StageStatus, WorkflowState
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
        if action is None:
            raise ValueError("No confirmable state action exists.")
        if action.action == "complete_topic":
            updated = state.model_copy(update={"stage_status": StageStatus.COMPLETED, "pending_action": None})
            self.repository.save_workflow_state(updated, "reflection_completed", {"stage": state.current_stage.value})
            self.repository.update_conversation_status(state.conversation_id, ConversationStatus.TOPIC_COMPLETED)
            return updated
        if action.action == "restart_cycle":
            updated = state.model_copy(
                update={"current_stage": Stage.DEFINITION, "stage_status": StageStatus.ACTIVE, "pending_action": None, "cycle_number": state.cycle_number + 1}
            )
            self.repository.save_workflow_state(updated, "reflection_cycle_restarted", {"cycle_number": updated.cycle_number})
            return updated
        if action.action == "branching":
            return self.clear_pending(state, "branch_parked")
        if action.target_stage is None:
            raise ValueError("Pending action has no target stage.")
        updated = state.model_copy(
            update={"current_stage": action.target_stage, "stage_status": StageStatus.ACTIVE, "pending_action": None}
        )
        self.repository.save_workflow_state(
            updated,
            "stage_changed",
            {"action": action.action, "from": state.current_stage.value, "to": action.target_stage.value},
        )
        return updated

    def confirm_topic_switch(self, state: WorkflowState, core_question: str) -> WorkflowState:
        self.repository.update_conversation_status(state.conversation_id, ConversationStatus.CLOSED)
        conversation = self.repository.create_conversation(core_question)
        return self.repository.get_workflow_state(conversation.id)
