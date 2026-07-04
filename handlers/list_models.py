from __future__ import annotations

from core.models_catalog import list_models
from models.inputs import ListModelsInput
from models.outputs import ListModelsResponse, ModelInfo


def handle_list_models(input: ListModelsInput) -> ListModelsResponse:
    return ListModelsResponse(
        models=[
            ModelInfo(
                model_id=model.model_id,
                label=model.label,
                task_type=model.task_type,
                cost_tier=model.cost_tier,
                recommended=model.recommended,
            )
            for model in list_models(input.task_type)
        ]
    )
