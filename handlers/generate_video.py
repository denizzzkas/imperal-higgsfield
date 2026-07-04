from __future__ import annotations

from clients.higgsfield_client import HiggsfieldProviderClient
from core.models_catalog import get_default_model, require_allowed_model
from core.normalize import normalize_request_record, normalize_thrown_error
from models.inputs import GenerateVideoInput
from models.outputs import NormalizedToolResponse


def handle_generate_video(input: GenerateVideoInput) -> NormalizedToolResponse:
    try:
        model = require_allowed_model(input.model_id, "video") if input.model_id else get_default_model("video")
        client = HiggsfieldProviderClient()
        record = client.submit_video(input.model_copy(update={"model_id": model.model_id}))
        return normalize_request_record(record)
    except Exception as error:
        return normalize_thrown_error(error)
