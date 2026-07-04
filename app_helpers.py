from __future__ import annotations

import os
from typing import Any


def current_secret_value(secret_obj: Any) -> str:
    return getattr(secret_obj, "value", None) or ""


def provider_env_from_runtime(secrets: dict[str, Any]) -> dict[str, str]:
    env = os.environ.copy()
    for key, value in secrets.items():
        env[key] = current_secret_value(value)
    return env
