from __future__ import annotations

from models.inputs import ListModelsInput
from models.outputs import ListModelsResponse
from handlers.list_models import handle_list_models


def test_list_models_returns_models() -> None:
    result = handle_list_models(ListModelsInput(task_type="all"))
    assert isinstance(result, ListModelsResponse)
    assert len(result.models) >= 1
