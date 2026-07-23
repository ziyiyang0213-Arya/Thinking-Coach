"""Pydantic models shared across the runtime."""

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Stage(StrEnum):
    DEFINITION = "definition"
    BUILDING = "building"
    REFINEMENT = "refinement"
    DEBATE = "debate"
    CLOSING = "closing"
    REFLECTION = "reflection"


class StageStatus(StrEnum):
    ACTIVE = "active"
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    COMPLETED = "completed"


class ConversationStatus(StrEnum):
    ACTIVE = "active"
    TOPIC_COMPLETED = "topic_completed"
    CLOSED = "closed"


class PendingAction(BaseModel):
    action: str
    target_stage: Stage | None = None
    reason: str
    required_inputs: list[str] = Field(default_factory=list)


class RuleDecision(BaseModel):
    rule: str
    action: str = "none"
    reason: str = "No state change requested."
    requires_confirmation: bool = False
    required_inputs: list[str] = Field(default_factory=list)
    memory_effects: list[str] = Field(default_factory=list)
    target_stage: Stage | None = None


class Conversation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    status: ConversationStatus = ConversationStatus.ACTIVE
    created_at: datetime = Field(default_factory=utc_now)
    closed_at: datetime | None = None


class WorkflowState(BaseModel):
    conversation_id: str
    current_stage: Stage = Stage.DEFINITION
    stage_status: StageStatus = StageStatus.ACTIVE
    pending_action: PendingAction | None = None
    cycle_number: int = 1


class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    conversation_id: str
    role: str
    content: str
    created_at: datetime = Field(default_factory=utc_now)


class LLMOutput(BaseModel):
    assistant_message: str
    extracted_facts: list[dict[str, Any]] = Field(default_factory=list)
    workflow_signal: str = "continue"
    proposed_actions: list[dict[str, Any]] = Field(default_factory=list)


class TurnResult(BaseModel):
    conversation_id: str
    assistant_message: str
    current_stage: Stage
    pending_action: PendingAction | None = None


class ReflectionRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    conversation_id: str
    version: int
    cycle_number: int
    data: dict[str, Any]
    created_at: datetime = Field(default_factory=utc_now)
