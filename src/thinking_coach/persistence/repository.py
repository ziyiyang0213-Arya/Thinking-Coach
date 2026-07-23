"""SQLite persistence. Only runtime services use this repository to commit state."""

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator

from thinking_coach.models import Conversation, ConversationStatus, Message, WorkflowState


def _timestamp(value: datetime) -> str:
    return value.isoformat()


class SQLiteRepository:
    def __init__(self, database_path: Path | str) -> None:
        self.database_path = str(database_path)

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self) -> None:
        with self.transaction() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    closed_at TEXT
                );
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL REFERENCES conversations(id),
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS topics (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL UNIQUE REFERENCES conversations(id),
                    core_question TEXT,
                    scope TEXT,
                    criteria TEXT,
                    status TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS workflow_states (
                    conversation_id TEXT PRIMARY KEY REFERENCES conversations(id),
                    current_stage TEXT NOT NULL,
                    stage_status TEXT NOT NULL,
                    pending_action_json TEXT,
                    cycle_number INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS memory_states (
                    conversation_id TEXT PRIMARY KEY REFERENCES conversations(id),
                    state_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS stage_snapshots (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL REFERENCES conversations(id),
                    stage TEXT NOT NULL,
                    cycle_number INTEGER NOT NULL,
                    data_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS reflections (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL REFERENCES conversations(id),
                    version INTEGER NOT NULL,
                    cycle_number INTEGER NOT NULL,
                    data_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE(conversation_id, version)
                );
                CREATE TABLE IF NOT EXISTS state_events (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL REFERENCES conversations(id),
                    event_type TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )

    def create_conversation(self) -> Conversation:
        conversation = Conversation()
        workflow_state = WorkflowState(conversation_id=conversation.id)
        with self.transaction() as connection:
            connection.execute(
                "INSERT INTO conversations (id, status, created_at, closed_at) VALUES (?, ?, ?, ?)",
                (conversation.id, conversation.status.value, _timestamp(conversation.created_at), None),
            )
            connection.execute(
                "INSERT INTO workflow_states VALUES (?, ?, ?, ?, ?)",
                (conversation.id, workflow_state.current_stage.value, workflow_state.stage_status.value, None, 1),
            )
            connection.execute(
                "INSERT INTO memory_states VALUES (?, ?)", (conversation.id, json.dumps({})),
            )
        return conversation

    def get_conversation(self, conversation_id: str) -> Conversation:
        with self.transaction() as connection:
            row = connection.execute("SELECT * FROM conversations WHERE id = ?", (conversation_id,)).fetchone()
        if row is None:
            raise KeyError(f"Conversation not found: {conversation_id}")
        return Conversation(
            id=row["id"], status=ConversationStatus(row["status"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            closed_at=datetime.fromisoformat(row["closed_at"]) if row["closed_at"] else None,
        )

    def get_workflow_state(self, conversation_id: str) -> WorkflowState:
        with self.transaction() as connection:
            row = connection.execute(
                "SELECT * FROM workflow_states WHERE conversation_id = ?", (conversation_id,)
            ).fetchone()
        if row is None:
            raise KeyError(f"Workflow state not found: {conversation_id}")
        return WorkflowState(
            conversation_id=conversation_id,
            current_stage=row["current_stage"],
            stage_status=row["stage_status"],
            pending_action=json.loads(row["pending_action_json"]) if row["pending_action_json"] else None,
            cycle_number=row["cycle_number"],
        )

    def save_workflow_state(self, state: WorkflowState, event_type: str, payload: dict[str, object]) -> None:
        from uuid import uuid4
        from thinking_coach.models.core import utc_now

        with self.transaction() as connection:
            connection.execute(
                """UPDATE workflow_states
                SET current_stage = ?, stage_status = ?, pending_action_json = ?, cycle_number = ?
                WHERE conversation_id = ?""",
                (
                    state.current_stage.value,
                    state.stage_status.value,
                    json.dumps(state.pending_action.model_dump(mode="json")) if state.pending_action else None,
                    state.cycle_number,
                    state.conversation_id,
                ),
            )
            connection.execute(
                "INSERT INTO state_events VALUES (?, ?, ?, ?, ?)",
                (str(uuid4()), state.conversation_id, event_type, json.dumps(payload), _timestamp(utc_now())),
            )

    def get_memory_state(self, conversation_id: str) -> dict[str, object]:
        with self.transaction() as connection:
            row = connection.execute(
                "SELECT state_json FROM memory_states WHERE conversation_id = ?", (conversation_id,)
            ).fetchone()
        if row is None:
            raise KeyError(f"Memory state not found: {conversation_id}")
        return json.loads(row["state_json"])

    def save_memory_state(self, conversation_id: str, state: dict[str, object]) -> None:
        with self.transaction() as connection:
            connection.execute(
                "UPDATE memory_states SET state_json = ? WHERE conversation_id = ?",
                (json.dumps(state), conversation_id),
            )

    def list_state_events(self, conversation_id: str) -> list[sqlite3.Row]:
        with self.transaction() as connection:
            return connection.execute(
                "SELECT * FROM state_events WHERE conversation_id = ? ORDER BY created_at", (conversation_id,)
            ).fetchall()

    def append_message(self, message: Message) -> None:
        with self.transaction() as connection:
            connection.execute(
                "INSERT INTO messages VALUES (?, ?, ?, ?, ?)",
                (message.id, message.conversation_id, message.role, message.content, _timestamp(message.created_at)),
            )

    def list_messages(self, conversation_id: str) -> list[Message]:
        with self.transaction() as connection:
            rows = connection.execute(
                "SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at", (conversation_id,)
            ).fetchall()
        return [
            Message(
                id=row["id"], conversation_id=row["conversation_id"], role=row["role"],
                content=row["content"], created_at=datetime.fromisoformat(row["created_at"]),
            )
            for row in rows
        ]
