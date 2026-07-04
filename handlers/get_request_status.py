from __future__ import annotations

from clients.higgsfield_client import HiggsfieldProviderClient
from core.normalize import normalize_request_record, normalize_thrown_error
from models.inputs import RequestStatusInput
from models.outputs import NormalizedToolResponse


def handle_get_request_status(input: RequestStatusInput) -> NormalizedToolResponse:
    try:
        client = HiggsfieldProviderClient()
        record = client.get_request(input.request_id)
        return normalize_request_record(record)
    except Exception as error:
        return normalize_thrown_error(error, input.request_id)
