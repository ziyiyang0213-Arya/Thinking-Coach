"""Runtime controller owns the persistence boundary and never delegates state commits to an LLM."""

from thinking_coach.llm import LLMClient
from thinking_coach.models import Message, PendingAction, TurnResult
from thinking_coach.persistence import SQLiteRepository
from thinking_coach.rule_engine import RuleEngine
from thinking_coach.memory import MemoryManager
from thinking_coach.state import StateManager
from thinking_coach.workflow_engine import WorkflowRegistry


class RuntimeController:
    def __init__(self, repository: SQLiteRepository, llm_client: LLMClient) -> None:
        self.repository = repository
        self.llm_client = llm_client
        self.rule_engine = RuleEngine()
        self.state_manager = StateManager(repository)
        self.workflows = WorkflowRegistry()
        self.memory_manager = MemoryManager(repository)

    def create_conversation(self) -> str:
        return self.repository.create_conversation().id

    def handle_turn(self, conversation_id: str, user_input: str) -> TurnResult:
        self.repository.get_conversation(conversation_id)
        workflow_state = self.repository.get_workflow_state(conversation_id)
        self.repository.append_message(Message(conversation_id=conversation_id, role="user", content=user_input))
        if workflow_state.pending_action:
            return self._resolve_pending(conversation_id, workflow_state, user_input)

        memory = self.repository.get_memory_state(conversation_id)
        pipeline = self.rule_engine.evaluate(workflow_state, memory, user_input)
        decision = pipeline.final_decision
        if decision.action == "deny":
            return self._respond(conversation_id, workflow_state, decision.reason)
        if decision.requires_confirmation:
            pending = PendingAction(
                action=decision.action,
                target_stage=decision.target_stage,
                reason=decision.reason,
                required_inputs=decision.required_inputs,
                data=decision.data,
            )
            updated = self.state_manager.set_pending(workflow_state, pending)
            return self._respond(
                conversation_id, updated, f"{decision.reason} Do you want to continue?"
            )

        if decision.action == "deepening":
            self.memory_manager.record_viewpoint_change(conversation_id, "deepening")

        handler = self.workflows.get(workflow_state.current_stage)
        output = self.llm_client.generate(handler.build_context(memory) + f"; user_input={user_input}")
        self.memory_manager.apply_current_state(conversation_id, output)
        return self._respond(conversation_id, workflow_state, output.assistant_message)

    def _resolve_pending(self, conversation_id: str, workflow_state, user_input: str) -> TurnResult:
        answer = user_input.strip().lower()
        if answer in {"yes", "y", "确认", "是"}:
            pending_action = workflow_state.pending_action
            if pending_action and pending_action.action == "topic_switch":
                core_question = str(pending_action.data["core_question"])
                new_state = self.state_manager.confirm_topic_switch(workflow_state, core_question)
                return self._respond(
                    new_state.conversation_id, new_state, f"Started a new Conversation for: {core_question}"
                )
            if pending_action and pending_action.action == "branching":
                self.memory_manager.record_branch(conversation_id, str(pending_action.data["description"]))
            self.memory_manager.snapshot_stage(workflow_state)
            updated = self.state_manager.confirm_pending(workflow_state)
            if pending_action and pending_action.action in {"complete_topic", "restart_cycle"}:
                record = self.memory_manager.finalize_reflection(workflow_state)
                if pending_action.action == "restart_cycle":
                    return self._respond(conversation_id, updated, f"Reflection v{record.version} saved. Started cycle {updated.cycle_number}.")
                return self._respond(conversation_id, updated, f"Reflection v{record.version} saved.")
            return self._respond(conversation_id, updated, f"Entered {updated.current_stage.value}.")
        if answer in {"no", "n", "取消", "否"}:
            updated = self.state_manager.clear_pending(workflow_state)
            return self._respond(conversation_id, updated, "Transition cancelled. We will remain in the current stage.")
        return self._respond(conversation_id, workflow_state, "Please confirm or reject the pending action.")

    def _respond(self, conversation_id: str, workflow_state, message: str) -> TurnResult:
        self.repository.append_message(
            Message(conversation_id=conversation_id, role="assistant", content=message)
        )
        return TurnResult(
            conversation_id=conversation_id,
            assistant_message=message,
            current_stage=workflow_state.current_stage,
            pending_action=workflow_state.pending_action,
        )
