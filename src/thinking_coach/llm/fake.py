"""Deterministic LLM used to validate controller behavior without network calls."""

from collections import deque

from thinking_coach.models import LLMOutput


class FakeLLMClient:
    def generate(self, context: str) -> LLMOutput:
        return LLMOutput(
            assistant_message="请先说明你希望深入思考的核心问题，以及你希望用什么标准判断它。",
            workflow_signal="continue",
        )


class ScriptedFakeLLMClient:
    """Returns explicitly supplied candidate outputs for deterministic session tests."""

    def __init__(self, outputs: list[LLMOutput]) -> None:
        self._outputs = deque(outputs)

    def generate(self, context: str) -> LLMOutput:
        if not self._outputs:
            raise AssertionError("No scripted LLM output remains for this workflow turn.")
        return self._outputs.popleft()
