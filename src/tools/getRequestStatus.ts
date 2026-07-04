import { normalizeRequestRecord, normalizeThrownError } from '../normalize.js';
import { HiggsfieldProviderClient } from '../provider.js';
import type { NormalizedToolResponse, RequestStatusInput } from '../types.js';

export async function getRequestStatus(input: RequestStatusInput): Promise<NormalizedToolResponse> {
  try {
    const client = new HiggsfieldProviderClient();
    const record = await client.getRequest(input.request_id);
    return normalizeRequestRecord(record);
  } catch (error) {
    return normalizeThrownError(error, input.request_id);
  }
}
