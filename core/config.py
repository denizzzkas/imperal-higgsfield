from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal, Mapping

from core.errors import HiggsfieldExtensionError

AuthMode = Literal["hf_key", "api_key_secret"]


@dataclass(slots=True)
class ProviderAuthConfig:
    mode: AuthMode
    hf_key: str | None = None
    api_key: str | None = None
    api_secret: str | None = None


@dataclass(slots=True)
class AppConfig:
    provider_base_url: str
    auth: ProviderAuthConfig


def load_config(env: Mapping[str, str | None] | None = None) -> AppConfig:
    source = env or os.environ
    provider_base_url = source.get("HIGGSFIELD_PROVIDER_BASE_URL") or "https://platform.higgsfield.ai"
    mode = source.get("HIGGSFIELD_PROVIDER_AUTH_MODE")

    if not mode:
        raise HiggsfieldExtensionError("AUTH_MISSING", "Missing HIGGSFIELD_PROVIDER_AUTH_MODE")

    if mode == "hf_key":
        hf_key = source.get("HIGGSFIELD_PROVIDER_HF_KEY")
        if not hf_key:
            raise HiggsfieldExtensionError("AUTH_MISSING", "Missing HIGGSFIELD_PROVIDER_HF_KEY")
        return AppConfig(provider_base_url=provider_base_url, auth=ProviderAuthConfig(mode=mode, hf_key=hf_key))

    if mode == "api_key_secret":
        api_key = source.get("HIGGSFIELD_PROVIDER_API_KEY")
        api_secret = source.get("HIGGSFIELD_PROVIDER_API_SECRET")
        if not api_key or not api_secret:
            raise HiggsfieldExtensionError(
                "AUTH_MISSING",
                "Missing HIGGSFIELD_PROVIDER_API_KEY or HIGGSFIELD_PROVIDER_API_SECRET",
            )
        return AppConfig(
            provider_base_url=provider_base_url,
            auth=ProviderAuthConfig(mode=mode, api_key=api_key, api_secret=api_secret),
        )

    raise HiggsfieldExtensionError("AUTH_INVALID", f"Unsupported auth mode: {mode}")
