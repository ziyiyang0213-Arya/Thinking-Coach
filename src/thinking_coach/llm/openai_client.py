"""OpenAI implementation of the candidate-only LLM interface."""

import json

from openai import OpenAI

from thinking_coach.models import LLMOutput


class OpenAILLMClient:
    def __init__(self, api_key: str, model: str) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, context: str) -> LLMOutput:
        response = self.client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "Return JSON with assistant_message, extracted_facts, workflow_signal, and proposed_actions. Do not claim to change application state.",
                },
                {"role": "user", "content": context},
            ],
        )
        content = response.choices[0].message.content
        if not content:
            raise ValueError("OpenAI returned an empty response.")
        return LLMOutput.model_validate(json.loads(content))
