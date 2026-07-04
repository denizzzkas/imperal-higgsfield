from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator


class GenerateImageInput(BaseModel):
    prompt: str = Field(..., min_length=1)
    model_id: str | None = None
    aspect_ratio: str | None = None
    negative_prompt: str | None = None
    seed: int | None = None


class GenerateVideoInput(BaseModel):
    model_id: str | None = None
    prompt: str | None = None
    image_url: str | None = None
    duration: int | None = None
    aspect_ratio: str | None = None

    @model_validator(mode="after")
    def ensure_some_source(self) -> "GenerateVideoInput":
        if not self.prompt and not self.image_url:
            raise ValueError("Either prompt or image_url is required")
        return self


class RequestStatusInput(BaseModel):
    request_id: str = Field(..., min_length=1)


class CancelRequestInput(BaseModel):
    request_id: str = Field(..., min_length=1)


class ListModelsInput(BaseModel):
    task_type: Literal["image", "video", "all"] = "all"
