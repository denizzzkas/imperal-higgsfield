from __future__ import annotations

from typing import Any

import httpx
import pytest

from clients.higgsfield_client import HiggsfieldProviderClient
from core.config import AppConfig, ProviderAuthConfig
from models.inputs import GenerateImageInput, GenerateVideoInput


class DummyResponse:
    def __init__(self, payload: dict[str, Any], status_code: int = 200) -> None:
        self._payload = payload
        self.status_code = status_code
        self.is_success = 200 <= status_code < 300

    def json(self) -> dict[str, Any]:
        return self._payload


class DummyClient:
    calls: list[dict[str, Any]] = []

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    def __enter__(self) -> "DummyClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def request(self, method: str, url: str, headers: dict[str, str], **kwargs: Any) -> DummyResponse:
        self.calls.append({"method": method, "url": url, "headers": headers, "kwargs": kwargs})
        if url.endswith("/status"):
            return DummyResponse({"request_id": "req_1", "status": "queued"})
        return DummyResponse({"request_id": "req_1", "status": "queued"})


def _make_client() -> HiggsfieldProviderClient:
    return HiggsfieldProviderClient(
        config=AppConfig(
            provider_base_url="https://platform.higgsfield.ai",
            auth=ProviderAuthConfig(mode="hf_key", hf_key="hf_test"),
        )
    )


def test_submit_image_uses_urlencoded_model_id(monkeypatch: pytest.MonkeyPatch) -> None:
    import pytest

    DummyClient.calls = []
    monkeypatch.setattr(httpx, "Client", DummyClient)
    client = _make_client()

    client.submit_image(
        GenerateImageInput(
            prompt="test",
            model_id="higgsfield-ai/soul/standard",
        )
    )

    assert DummyClient.calls[0]["method"] == "POST"
    assert DummyClient.calls[0]["url"] == "https://platform.higgsfield.ai/higgsfield-ai%2Fsoul%2Fstandard"


def test_submit_video_uses_urlencoded_model_id(monkeypatch: pytest.MonkeyPatch) -> None:
    import pytest

    DummyClient.calls = []
    monkeypatch.setattr(httpx, "Client", DummyClient)
    client = _make_client()

    client.submit_video(
        GenerateVideoInput(
            prompt="animate this",
            model_id="bytedance/seedance/v1/pro/image-to-video",
        )
    )

    assert DummyClient.calls[0]["method"] == "POST"
    assert DummyClient.calls[0]["url"] == "https://platform.higgsfield.ai/bytedance%2Fseedance%2Fv1%2Fpro%2Fimage-to-video"


def test_get_request_status_path(monkeypatch: pytest.MonkeyPatch) -> None:
    import pytest

    DummyClient.calls = []
    monkeypatch.setattr(httpx, "Client", DummyClient)
    client = _make_client()

    client.get_request("req_67890")

    assert DummyClient.calls[0]["method"] == "GET"
    assert DummyClient.calls[0]["url"] == "https://platform.higgsfield.ai/requests/req_67890/status"


def test_cancel_request_path(monkeypatch: pytest.MonkeyPatch) -> None:
    import pytest

    DummyClient.calls = []
    monkeypatch.setattr(httpx, "Client", DummyClient)
    client = _make_client()

    client.cancel_request("req_67890")

    assert DummyClient.calls[0]["method"] == "POST"
    assert DummyClient.calls[0]["url"] == "https://platform.higgsfield.ai/requests/req_67890/cancel"
