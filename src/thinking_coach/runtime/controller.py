"""Runtime controller owns the persistence boundary and never delegates state commits to an LLM."""

from thinking_coach.llm import LLMClient
from thinking_coach.models import Message, TurnResult
from thinking_coach.persistence import SQLiteRepository


class RuntimeController:
    def __init__(self, repository: SQLiteRepository, llm_client: LLMClient) -> None:
        self.repository = repository
        self.llm_client = llm_client

    def create_conversation(self) -> str:
        return self.repository.create_conversation().id

    def handle_turn(self, conversation_id: str, user_input: str) -> TurnResult:
        self.repository.get_conversation(conversation_id)
        workflow_state = self.repository.get_workflow_state(conversation_id)
        self.repository.append_message(Message(conversation_id=conversation_id, role="user", content=user_input))
        output = self.llm_client.generate(
            f"stage={workflow_state.current_stage}; user_input={user_input}"
        )
        self.repository.append_message(
            Message(conversation_id=conversation_id, role="assistant", content=output.assistant_message)
        )
        return TurnResult(
            conversation_id=conversation_id,
            assistant_message=output.assistant_message,
            current_stage=workflow_state.current_stage,
            pending_action=workflow_state.pending_action,
        )
