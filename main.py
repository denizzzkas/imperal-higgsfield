from __future__ import annotations

from imperal_sdk import ChatExtension, Extension, tool  # type: ignore

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


extension = Extension(
    app_id="imperal-higgsfield",
    name="Imperal Higgsfield",
    description="Managed Higgsfield Cloud image and video generation for Imperal.",
)

chat_extension = ChatExtension(
    app_id="imperal-higgsfield",
    name="Imperal Higgsfield",
    description="Managed Higgsfield Cloud image and video generation for Imperal.",
)


@tool(name="hf_generate_image", description="Generate an image with Higgsfield Cloud.")
def hf_generate_image(input: GenerateImageInput):
    return handle_generate_image(input).model_dump(exclude_none=True)


@tool(name="hf_generate_video", description="Generate a video with Higgsfield Cloud.")
def hf_generate_video(input: GenerateVideoInput):
    return handle_generate_video(input).model_dump(exclude_none=True)


@tool(name="hf_get_request_status", description="Check status of a Higgsfield generation request.")
def hf_get_request_status(input: RequestStatusInput):
    return handle_get_request_status(input).model_dump(exclude_none=True)


@tool(name="hf_cancel_request", description="Cancel a Higgsfield request if the provider still allows it.")
def hf_cancel_request(input: CancelRequestInput):
    return handle_cancel_request(input).model_dump(exclude_none=True)


@tool(name="hf_list_models", description="List the curated Higgsfield model catalog exposed by this extension.")
def hf_list_models(input: ListModelsInput):
    return handle_list_models(input).model_dump(exclude_none=True)
