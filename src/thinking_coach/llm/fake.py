"""Deterministic LLM used to validate controller behavior without network calls."""

from thinking_coach.models import LLMOutput


class FakeLLMClient:
    def generate(self, context: str) -> LLMOutput:
        return LLMOutput(
            assistant_message="请先说明你希望深入思考的核心问题，以及你希望用什么标准判断它。",
            workflow_signal="continue",
        )
