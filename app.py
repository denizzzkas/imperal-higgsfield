from __future__ import annotations

from imperal_sdk import Extension

from core.models_catalog import MODELS

from handlers.cancel_request import handle_cancel_request
from handlers.generate_image import handle_generate_image
from handlers.generate_video import handle_generate_video
from handlers.get_request_status import handle_get_request_status
from handlers.list_models import handle_list_models
from models.inputs import (
    CancelRequestInput,
    GenerateImageInput,
    GenerateVideoInput,
    ListModelsInput,
    RequestStatusInput,
)


ext = Extension(
    app_id="higgsfield-extension",
    version="0.1.0",
    display_name="Imperal Higgsfield",
    description="Managed Higgsfield Cloud media generation extension for Imperal.",
    icon="icon.svg",
)


@ext.tool("hf_generate_image", description="Generate an image with Higgsfield Cloud.")
def hf_generate_image(input: GenerateImageInput):
    return handle_generate_image(input).model_dump(exclude_none=True)


@ext.tool("hf_generate_video", description="Generate a video with Higgsfield Cloud.")
def hf_generate_video(input: GenerateVideoInput):
    return handle_generate_video(input).model_dump(exclude_none=True)


@ext.tool(
    "hf_get_request_status",
    description="Check status of a Higgsfield generation request.",
)
def hf_get_request_status(input: RequestStatusInput):
    return handle_get_request_status(input).model_dump(exclude_none=True)


@ext.tool(
    "hf_cancel_request",
    description="Cancel a Higgsfield request if the provider still allows it.",
)
def hf_cancel_request(input: CancelRequestInput):
    return handle_cancel_request(input).model_dump(exclude_none=True)


@ext.tool(
    "hf_list_models",
    description="List the curated Higgsfield model catalog exposed by this extension.",
)
def hf_list_models(input: ListModelsInput):
    return handle_list_models(input).model_dump(exclude_none=True)


@ext.health_check
def health_check():
    return {
        "ok": True,
        "service": "imperal-higgsfield",
        "tools": 5,
        "models_available": len(MODELS),
    }


@ext.on_install
def on_install():
    return {
        "ok": True,
        "message": "Imperal Higgsfield installed successfully.",
    }


__all__ = ["ext"]
