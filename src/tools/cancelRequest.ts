import { mapUnknownError } from '../errors.js';
import { normalizeCancelRecord } from '../normalize.js';
import { HiggsfieldProviderClient } from '../provider.js';
import type { CancelRequestInput, CancelToolResponse } from '../types.js';

export async function cancelRequest(input: CancelRequestInput): Promise<CancelToolResponse> {
  try {
    const client = new HiggsfieldProviderClient();
    const record = await client.cancelRequest(input.request_id);
    return normalizeCancelRecord(record);
  } catch (error) {
    const mapped = mapUnknownError(error);
    return {
      request_id: input.request_id,
      cancelled: false,
      provider_status: mapped.code,
    };
  }
}
