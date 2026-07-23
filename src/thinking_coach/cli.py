"""Command-line interface for the Thinking Coach runtime."""

import argparse

from thinking_coach.config import Settings
from thinking_coach.llm import FakeLLMClient
from thinking_coach.persistence import SQLiteRepository
from thinking_coach.runtime import RuntimeController


def build_controller(database_path: str | None) -> RuntimeController:
    settings = Settings.from_environment(database_path)
    repository = SQLiteRepository(settings.database_path)
    repository.initialize()
    return RuntimeController(repository, FakeLLMClient())


def main() -> None:
    parser = argparse.ArgumentParser(prog="thinking-coach")
    parser.add_argument("--database", help="SQLite database path")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("start")
    chat = subparsers.add_parser("chat")
    chat.add_argument("conversation_id")
    chat.add_argument("message")
    args = parser.parse_args()
    controller = build_controller(args.database)

    if args.command == "start":
        print(controller.create_conversation())
        return

    result = controller.handle_turn(args.conversation_id, args.message)
    print(result.assistant_message)
    print(f"stage={result.current_stage}")
