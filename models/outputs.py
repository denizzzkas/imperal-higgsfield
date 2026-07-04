from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

NormalizedStatus = Literal["pending", "running", "succeeded", "failed", "blocked", "cancelled"]


class NormalizedToolResponse(BaseModel):
    request_id: str
    normalized_status: NormalizedStatus
    provider_status: str
    model_id: str | None = None
    result_urls: list[str] = []
    error_code: str | None = None
    error_message: str | None = None
    refunded: bool | None = None


class CancelToolResponse(BaseModel):
    request_id: str
    cancelled: bool
    provider_status: str


class ModelInfo(BaseModel):
    model_id: str
    label: str
    task_type: Literal["image", "video"]
    cost_tier: str
    recommended: bool


class ListModelsResponse(BaseModel):
    models: list[ModelInfo]


class ProviderErrorInfo(BaseModel):
    code: str | None = None
    message: str | None = None


class ProviderRequestRecord(BaseModel):
    id: str
    status: str
    model: str | None = None
    output: list[str] | None = None
    error: ProviderErrorInfo | None = None


class ProviderImageResponse(BaseModel):
    request_id: str
    status: str
    result_url: str | None = None
    result_urls: list[str] | None = None
    detail: object | None = None


class ProviderVideoResponse(BaseModel):
    request_id: str
    status: str
    result_url: str | None = None
    result_urls: list[str] | None = None
    detail: object | None = None


class ProviderStatusResponse(BaseModel):
    request_id: str | None = None
    status: str
    model_id: str | None = None
    result_url: str | None = None
    result_urls: list[str] | None = None
    detail: object | None = None
