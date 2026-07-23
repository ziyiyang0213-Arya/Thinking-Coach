"""Explicit stage machine and minimum input validation."""

from thinking_coach.models import Stage


STAGE_ORDER = [
    Stage.DEFINITION,
    Stage.BUILDING,
    Stage.REFINEMENT,
    Stage.DEBATE,
    Stage.CLOSING,
    Stage.REFLECTION,
]


def next_stage(stage: Stage) -> Stage | None:
    index = STAGE_ORDER.index(stage)
    return STAGE_ORDER[index + 1] if index + 1 < len(STAGE_ORDER) else None


def required_inputs_for(stage: Stage, memory: dict[str, object]) -> list[str]:
    required: dict[Stage, list[tuple[str, str]]] = {
        Stage.BUILDING: [("core_question", "Core Question")],
        Stage.REFINEMENT: [("user_position", "User Position"), ("basic_reasoning", "Basic Reasoning")],
        Stage.DEBATE: [
            ("user_position", "User Position"),
            ("reasoning", "Reasoning"),
            ("arguments", "at least one Argument"),
        ],
        Stage.CLOSING: [("debate_completed", "completed Debate or explicit end request")],
        Stage.REFLECTION: [("original_thinking", "Original Thinking"), ("current_thinking", "Current Thinking")],
    }
    missing: list[str] = []
    for key, label in required.get(stage, []):
        value = memory.get(key)
        if not value:
            missing.append(label)
    return missing


def can_enter(current_stage: Stage, target_stage: Stage, memory: dict[str, object]) -> tuple[bool, list[str]]:
    if current_stage is Stage.DEBATE and target_stage is Stage.REFINEMENT:
        return True, []
    if target_stage not in STAGE_ORDER or STAGE_ORDER.index(target_stage) <= STAGE_ORDER.index(current_stage):
        return False, ["target stage must be forward, except Debate → Refinement"]
    missing = required_inputs_for(target_stage, memory)
    return not missing, missing
