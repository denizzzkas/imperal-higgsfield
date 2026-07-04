from __future__ import annotations

from clients.higgsfield_client import HiggsfieldProviderClient
from core.models_catalog import get_default_model, require_allowed_model
from core.normalize import normalize_request_record, normalize_thrown_error
from models.inputs import GenerateImageInput
from models.outputs import NormalizedToolResponse


def handle_generate_image(input: GenerateImageInput) -> NormalizedToolResponse:
    try:
        model = require_allowed_model(input.model_id, "image") if input.model_id else get_default_model("image")
        client = HiggsfieldProviderClient()
        record = client.submit_image(input.model_copy(update={"model_id": model.model_id}))
        return normalize_request_record(record)
    except Exception as error:
        return normalize_thrown_error(error)
