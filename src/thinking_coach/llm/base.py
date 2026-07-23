"""LLM abstraction. Implementations return candidates, never persisted state changes."""

from typing import Protocol

from thinking_coach.models import LLMOutput


class LLMClient(Protocol):
    def generate(self, context: str) -> LLMOutput: ...
