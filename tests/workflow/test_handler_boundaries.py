from thinking_coach.models import Stage
from thinking_coach.workflow_engine import WorkflowRegistry


def test_workflow_handlers_encode_stage_boundaries_without_state_methods() -> None:
    handlers = WorkflowRegistry()

    assert "Do not create the user's position." in handlers.get(Stage.BUILDING).restrictions
    assert "Do not adopt an opponent role." in handlers.get(Stage.REFINEMENT).restrictions
    assert "Do not supply missing arguments for the user." in handlers.get(Stage.DEBATE).restrictions
    assert "Challenge only user-expressed claims, reasoning, assumptions, and boundaries." in handlers.get(Stage.DEBATE).restrictions
    assert "Do not write the user's closing statement." in handlers.get(Stage.CLOSING).restrictions
    assert "Do not add unexpressed insights or evaluate growth." in handlers.get(Stage.REFLECTION).restrictions
    assert not hasattr(handlers.get(Stage.DEBATE), "transition")
