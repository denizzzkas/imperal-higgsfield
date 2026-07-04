from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

CanonicalErrorCode = Literal[
    "AUTH_MISSING",
    "AUTH_INVALID",
    "INSUFFICIENT_PROVIDER_BALANCE",
    "RATE_LIMITED",
    "MODEL_NOT_FOUND",
    "INVALID_INPUT",
    "REQUEST_FAILED",
    "REQUEST_BLOCKED_NSFW",
    "REQUEST_CANCELLED",
    "NETWORK_ERROR",
    "UNKNOWN_PROVIDER_ERROR",
]


@dataclass(slots=True)
class HiggsfieldExtensionError(Exception):
    code: CanonicalErrorCode
    message: str
    provider_status: int | None = None

    def __str__(self) -> str:
        return self.message


def map_unknown_error(error: object) -> HiggsfieldExtensionError:
    if isinstance(error, HiggsfieldExtensionError):
        return error

    if isinstance(error, Exception):
        return HiggsfieldExtensionError("UNKNOWN_PROVIDER_ERROR", str(error))

    return HiggsfieldExtensionError("UNKNOWN_PROVIDER_ERROR", "Unknown provider error")
