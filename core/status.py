from __future__ import annotations

from models.outputs import NormalizedStatus

_STATUS_MAP: dict[str, NormalizedStatus] = {
    "queued": "pending",
    "pending": "pending",
    "in_progress": "running",
    "processing": "running",
    "completed": "succeeded",
    "succeeded": "succeeded",
    "failed": "failed",
    "nsfw": "blocked",
    "blocked": "blocked",
    "cancelled": "cancelled",
    "canceled": "cancelled",
}


def normalize_status(provider_status: str) -> NormalizedStatus:
    return _STATUS_MAP.get(provider_status, "failed")
