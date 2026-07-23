"""Structured memory updates and immutable stage/reflection snapshots."""

from uuid import uuid4

from thinking_coach.models import LLMOutput, ReflectionRecord, Stage, WorkflowState
from thinking_coach.models.core import utc_now
from thinking_coach.persistence import SQLiteRepository


class MemoryManager:
    FACT_KEYS = {
        "core_question", "scope", "criteria", "original_thinking", "user_position",
        "basic_reasoning", "reasoning", "arguments", "refined_argument", "assumptions",
        "responses", "debate_completed", "current_thinking", "remaining_questions",
    }

    def __init__(self, repository: SQLiteRepository) -> None:
        self.repository = repository

    def apply_current_state(self, conversation_id: str, output: LLMOutput) -> dict[str, object]:
        memory = self.repository.get_memory_state(conversation_id)
        for fact in output.extracted_facts:
            key = fact.get("key")
            if key in self.FACT_KEYS and "value" in fact:
                memory[str(key)] = fact["value"]
        self.repository.save_memory_state(conversation_id, memory)
        return memory

    def snapshot_stage(self, workflow_state: WorkflowState) -> None:
        data = self.repository.get_memory_state(workflow_state.conversation_id)
        self.repository.create_stage_snapshot(
            str(uuid4()), workflow_state.conversation_id, workflow_state.current_stage.value,
            workflow_state.cycle_number, data, utc_now(),
        )

    def finalize_reflection(self, workflow_state: WorkflowState) -> ReflectionRecord:
        if workflow_state.current_stage is not Stage.REFLECTION:
            raise ValueError("Reflection can only be finalized from the reflection stage.")
        memory = self.repository.get_memory_state(workflow_state.conversation_id)
        record_data = {
            key: memory.get(key)
            for key in ("original_thinking", "current_thinking", "thinking_evolution", "key_drivers", "remaining_questions")
            if key in memory
        }
        version = len(self.repository.list_reflections(workflow_state.conversation_id)) + 1
        record = ReflectionRecord(
            conversation_id=workflow_state.conversation_id,
            version=version,
            cycle_number=workflow_state.cycle_number,
            data=record_data,
        )
        self.repository.create_reflection(record)
        return record
