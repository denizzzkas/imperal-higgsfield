from __future__ import annotations

from typing import Any
from urllib.parse import quote

import httpx

from core.config import AppConfig, load_config
from core.errors import HiggsfieldExtensionError
from models.inputs import GenerateImageInput, GenerateVideoInput
from models.outputs import (
    ProviderErrorInfo,
    ProviderImageResponse,
    ProviderRequestRecord,
    ProviderStatusResponse,
    ProviderVideoResponse,
)


class HiggsfieldProviderClient:
    def __init__(self, config: AppConfig | None = None, timeout: float = 60.0) -> None:
        self.config = config or load_config()
        self.timeout = timeout

    def submit_image(self, input: GenerateImageInput) -> ProviderRequestRecord:
        if not input.model_id:
            raise HiggsfieldExtensionError("INVALID_INPUT", "Missing model_id for image request")
        payload = self._post(f"/{quote(input.model_id, safe='')}", input.model_dump(exclude_none=True))
        return _map_image_response(ProviderImageResponse.model_validate(payload), input.model_id)

    def submit_video(self, input: GenerateVideoInput) -> ProviderRequestRecord:
        if not input.model_id:
            raise HiggsfieldExtensionError("INVALID_INPUT", "Missing model_id for video request")
        payload = self._post(f"/{quote(input.model_id, safe='')}", input.model_dump(exclude_none=True))
        return _map_video_response(ProviderVideoResponse.model_validate(payload), input.model_id)

    def get_request(self, request_id: str) -> ProviderRequestRecord:
        payload = self._get(f"/requests/{request_id}/status")
        return _map_status_response(ProviderStatusResponse.model_validate(payload), request_id)

    def cancel_request(self, request_id: str) -> ProviderRequestRecord:
        payload = self._post(f"/requests/{request_id}/cancel", {})
        return _map_status_response(ProviderStatusResponse.model_validate(payload), request_id)

    def _build_headers(self) -> dict[str, str]:
        if self.config.auth.mode == "hf_key":
            return {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config.auth.hf_key}",
            }
        return {
            "Content-Type": "application/json",
            "X-API-Key": self.config.auth.api_key or "",
            "X-API-Secret": self.config.auth.api_secret or "",
        }

    def _get(self, path: str) -> dict[str, Any]:
        return self._request("GET", path)

    def _post(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", path, json=body)

    def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        url = f"{self.config.provider_base_url}{path}"
        headers = self._build_headers()
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.request(method, url, headers=headers, **kwargs)
        except httpx.HTTPError as exc:
            raise HiggsfieldExtensionError("NETWORK_ERROR", str(exc)) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise HiggsfieldExtensionError(
                "NETWORK_ERROR",
                "Provider returned a non-JSON response",
                response.status_code,
            ) from exc

        if not response.is_success:
            raise self._map_provider_http_error(response.status_code, payload)

        if not isinstance(payload, dict):
            raise HiggsfieldExtensionError("NETWORK_ERROR", "Provider returned an invalid JSON payload", response.status_code)

        return payload

    def _map_provider_http_error(self, status: int, payload: Any) -> HiggsfieldExtensionError:
        message = _extract_message(payload) or f"Provider request failed with status {status}"
        if status in (401, 403):
            return HiggsfieldExtensionError("AUTH_INVALID", message, status)
        if status == 402:
            return HiggsfieldExtensionError("INSUFFICIENT_PROVIDER_BALANCE", message, status)
        if status in (400, 422):
            return HiggsfieldExtensionError("INVALID_INPUT", message, status)
        if status == 429:
            return HiggsfieldExtensionError("RATE_LIMITED", message, status)
        return HiggsfieldExtensionError("REQUEST_FAILED", message, status)


def _map_image_response(payload: ProviderImageResponse, model_id: str | None) -> ProviderRequestRecord:
    return ProviderRequestRecord(
        id=payload.request_id,
        status=payload.status,
        model=model_id,
        output=_collect_result_urls(payload.result_url, payload.result_urls),
        error=_extract_embedded_error(payload.detail),
    )


def _map_video_response(payload: ProviderVideoResponse, model_id: str | None) -> ProviderRequestRecord:
    return ProviderRequestRecord(
        id=payload.request_id,
        status=payload.status,
        model=model_id,
        output=_collect_result_urls(payload.result_url, payload.result_urls),
        error=_extract_embedded_error(payload.detail),
    )


def _map_status_response(payload: ProviderStatusResponse, request_id: str) -> ProviderRequestRecord:
    return ProviderRequestRecord(
        id=payload.request_id or request_id,
        status=payload.status,
        model=payload.model_id,
        output=_collect_result_urls(payload.result_url, payload.result_urls),
        error=_extract_embedded_error(payload.detail),
    )


def _collect_result_urls(result_url: str | None, result_urls: list[str] | None) -> list[str] | None:
    urls = [url for url in (result_urls or []) if isinstance(url, str) and url.strip()]
    if urls:
        return urls
    if result_url and result_url.strip():
        return [result_url]
    return None


def _extract_embedded_error(detail: object | None) -> ProviderErrorInfo | None:
    if isinstance(detail, str) and detail.strip():
        return ProviderErrorInfo(message=detail)
    if isinstance(detail, dict):
        message = detail.get("message")
        fallback = detail.get("detail")
        return ProviderErrorInfo(
            message=message if isinstance(message, str) else fallback if isinstance(fallback, str) else None,
        )
    return None


def _extract_message(payload: Any) -> str | None:
    if not isinstance(payload, dict):
        return None
    maybe_message = payload.get("message")
    if isinstance(maybe_message, str) and maybe_message.strip():
        return maybe_message
    maybe_detail = payload.get("detail")
    if isinstance(maybe_detail, str) and maybe_detail.strip():
        return maybe_detail
    maybe_error = payload.get("error")
    if isinstance(maybe_error, str) and maybe_error.strip():
        return maybe_error
    if isinstance(maybe_error, dict):
        nested_message = maybe_error.get("message")
        if isinstance(nested_message, str) and nested_message.strip():
            return nested_message
    return None
