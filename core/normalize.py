from __future__ import annotations

from core.errors import map_unknown_error
from core.status import normalize_status
from models.outputs import CancelToolResponse, NormalizedToolResponse, ProviderRequestRecord


def normalize_request_record(record: ProviderRequestRecord) -> NormalizedToolResponse:
    normalized_status = normalize_status(record.status)

    return NormalizedToolResponse(
        request_id=record.id,
        normalized_status=normalized_status,
        provider_status=record.status,
        model_id=record.model,
        result_urls=record.output or [],
        error_code=(record.error.code if record.error else None) or _default_error_code_for_status(normalized_status),
        error_message=record.error.message if record.error else None,
        refunded=normalized_status in {"failed", "blocked"},
    )


def normalize_cancel_record(record: ProviderRequestRecord) -> CancelToolResponse:
    return CancelToolResponse(
        request_id=record.id,
        cancelled=normalize_status(record.status) == "cancelled",
        provider_status=record.status,
    )


def normalize_thrown_error(error: object, request_id: str = "") -> NormalizedToolResponse:
    mapped = map_unknown_error(error)
    return NormalizedToolResponse(
        request_id=request_id,
        normalized_status="failed",
        provider_status="error",
        result_urls=[],
        error_code=mapped.code,
        error_message=mapped.message,
        refunded=False,
    )


def _default_error_code_for_status(normalized_status: NormalizedToolResponse.model_fields["normalized_status"].annotation) -> str | None:
    if normalized_status == "blocked":
        return "REQUEST_BLOCKED_NSFW"
    if normalized_status == "cancelled":
        return "REQUEST_CANCELLED"
    if normalized_status == "failed":
        return "REQUEST_FAILED"
    return None
