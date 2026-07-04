from __future__ import annotations

from clients.higgsfield_client import HiggsfieldProviderClient
from core.errors import map_unknown_error
from core.normalize import normalize_cancel_record
from models.inputs import CancelRequestInput
from models.outputs import CancelToolResponse


def handle_cancel_request(input: CancelRequestInput) -> CancelToolResponse:
    try:
        client = HiggsfieldProviderClient()
        record = client.cancel_request(input.request_id)
        return normalize_cancel_record(record)
    except Exception as error:
        mapped = map_unknown_error(error)
        return CancelToolResponse(
            request_id=input.request_id,
            cancelled=False,
            provider_status=mapped.code,
        )
