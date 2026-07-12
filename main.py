from __future__ import annotations

from imperal_sdk import Extension, ui

from core.models_catalog import MODELS, list_models

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


@ext.panel(
    "overview",
    title="Higgsfield Overview",
    icon="sparkles",
    slot="center",
)
def overview_panel():
    available_models = list_models("all")
    model_cards = []
    for model in available_models[:6]:
        model_cards.append(
            ui.Card(
                title=model.label,
                subtitle=model.model_id,
                content=ui.Stack(
                    [
                        ui.Badge(model.task_type, color="blue" if model.task_type == "image" else "purple"),
                        ui.Badge(model.cost_tier, color="gray"),
                        ui.Text(
                            "Recommended" if model.recommended else "Available",
                            variant="muted",
                        ),
                    ],
                    gap=2,
                ),
            )
        )

    return ui.Page(
        title="Imperal Higgsfield",
        subtitle="Tiny control room for media generation in Imperal.",
        children=[
            ui.Section(
                title="Status",
                children=[
                    ui.Grid(
                        columns=3,
                        children=[
                            ui.Stat("Health", "OK", icon="heartbeat", color="green"),
                            ui.Stat("Tools", 5, icon="tool", color="blue"),
                            ui.Stat("Models", len(available_models), icon="layers", color="purple"),
                        ],
                    )
                ],
            ),
            ui.Section(
                title="Quick actions",
                children=[
                    ui.Stack(
                        direction="h",
                        gap=2,
                        wrap=True,
                        children=[
                            ui.Button(
                                "Open Imperal panel",
                                variant="primary",
                                on_click=ui.Open("https://panel.imperal.io"),
                                icon="external-link",
                            ),
                            ui.Button(
                                "Ask to list models",
                                variant="secondary",
                                on_click=ui.Send("List Higgsfield models available in this extension"),
                                icon="message-square",
                            ),
                            ui.Button(
                                "Ask to generate image",
                                variant="secondary",
                                on_click=ui.Send("Generate an image with Higgsfield using my prompt"),
                                icon="image",
                            ),
                            ui.Button(
                                "Ask to generate video",
                                variant="secondary",
                                on_click=ui.Send("Generate a video with Higgsfield using my prompt"),
                                icon="video",
                            ),
                        ],
                    )
                ],
            ),
            ui.Section(
                title="Model catalog",
                children=[
                    ui.Text("A small preview of the curated catalog exposed by the extension."),
                    ui.Grid(children=model_cards, columns=2),
                ],
            ),
        ],
    )


__all__ = ["ext"]
