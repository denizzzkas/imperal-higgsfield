from __future__ import annotations

import pytest

from core.config import load_config
from core.errors import HiggsfieldExtensionError
from core.status import normalize_status


def test_load_config_hf_key_mode() -> None:
    config = load_config(
        {
            "HIGGSFIELD_PROVIDER_AUTH_MODE": "hf_key",
            "HIGGSFIELD_PROVIDER_HF_KEY": "hf_test_key",
        }
    )
    assert config.provider_base_url == "https://platform.higgsfield.ai"
    assert config.auth.mode == "hf_key"
    assert config.auth.hf_key == "hf_test_key"


def test_load_config_api_key_secret_mode() -> None:
    config = load_config(
        {
            "HIGGSFIELD_PROVIDER_AUTH_MODE": "api_key_secret",
            "HIGGSFIELD_PROVIDER_API_KEY": "key123",
            "HIGGSFIELD_PROVIDER_API_SECRET": "secret123",
            "HIGGSFIELD_PROVIDER_BASE_URL": "https://example.higgsfield.test",
        }
    )
    assert config.provider_base_url == "https://example.higgsfield.test"
    assert config.auth.mode == "api_key_secret"
    assert config.auth.api_key == "key123"
    assert config.auth.api_secret == "secret123"


def test_load_config_rejects_unknown_mode() -> None:
    with pytest.raises(HiggsfieldExtensionError) as exc:
        load_config({"HIGGSFIELD_PROVIDER_AUTH_MODE": "nope"})
    assert exc.value.code == "AUTH_INVALID"


def test_normalize_status_mapping() -> None:
    assert normalize_status("queued") == "pending"
    assert normalize_status("in_progress") == "running"
    assert normalize_status("completed") == "succeeded"
    assert normalize_status("failed") == "failed"
    assert normalize_status("nsfw") == "blocked"
    assert normalize_status("cancelled") == "cancelled"
    assert normalize_status("canceled") == "cancelled"
    assert normalize_status("unexpected") == "failed"
