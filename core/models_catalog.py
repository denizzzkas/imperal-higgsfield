from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from core.errors import HiggsfieldExtensionError

HiggsfieldTaskType = Literal["image", "video"]


@dataclass(frozen=True, slots=True)
class ModelDefinition:
    model_id: str
    label: str
    task_type: HiggsfieldTaskType
    cost_tier: str
    recommended: bool
    enabled: bool


MODELS: tuple[ModelDefinition, ...] = (
    ModelDefinition(
        model_id="reve/text-to-image",
        label="Fast Image",
        task_type="image",
        cost_tier="image_basic",
        recommended=True,
        enabled=True,
    ),
    ModelDefinition(
        model_id="higgsfield-ai/soul/standard",
        label="Higgsfield Soul",
        task_type="image",
        cost_tier="image_pro",
        recommended=True,
        enabled=True,
    ),
    ModelDefinition(
        model_id="higgsfield-ai/dop/preview",
        label="Higgsfield Dop",
        task_type="video",
        cost_tier="video_basic",
        recommended=False,
        enabled=True,
    ),
    ModelDefinition(
        model_id="bytedance/seedance/v1/pro/image-to-video",
        label="Seedance Image to Video",
        task_type="video",
        cost_tier="video_pro",
        recommended=True,
        enabled=True,
    ),
    ModelDefinition(
        model_id="kling-video/v2.1/pro/image-to-video",
        label="Kling 2.1 Image to Video",
        task_type="video",
        cost_tier="video_pro",
        recommended=False,
        enabled=True,
    ),
)


def list_models(task_type: HiggsfieldTaskType | Literal["all"] = "all") -> list[ModelDefinition]:
    return [model for model in MODELS if model.enabled and (task_type == "all" or model.task_type == task_type)]


def get_default_model(task_type: HiggsfieldTaskType) -> ModelDefinition:
    for model in MODELS:
        if model.task_type == task_type and model.recommended and model.enabled:
            return model
    raise HiggsfieldExtensionError("REQUEST_FAILED", f"No enabled default model for task type: {task_type}")


def require_allowed_model(model_id: str, task_type: HiggsfieldTaskType) -> ModelDefinition:
    for model in MODELS:
        if model.model_id == model_id and model.task_type == task_type and model.enabled:
            return model
    raise HiggsfieldExtensionError("MODEL_NOT_FOUND", f"Model not allowed: {model_id}")
