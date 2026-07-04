import { mapUnknownError } from './errors.js';
import { normalizeStatus } from './status.js';
import type { CancelToolResponse, NormalizedToolResponse, ProviderRequestRecord } from './types.js';

export function normalizeRequestRecord(record: ProviderRequestRecord): NormalizedToolResponse {
  const normalizedStatus = normalizeStatus(record.status);

  return {
    request_id: record.id,
    normalized_status: normalizedStatus,
    provider_status: record.status,
    model_id: record.model,
    result_urls: record.output ?? [],
    error_code: record.error?.code ?? defaultErrorCodeForStatus(normalizedStatus),
    error_message: record.error?.message,
    refunded: normalizedStatus === 'failed' || normalizedStatus === 'blocked',
  };
}

export function normalizeCancelRecord(record: ProviderRequestRecord): CancelToolResponse {
  return {
    request_id: record.id,
    cancelled: normalizeStatus(record.status) === 'cancelled',
    provider_status: record.status,
  };
}

export function normalizeThrownError(error: unknown, requestId = ''): NormalizedToolResponse {
  const mapped = mapUnknownError(error);
  return {
    request_id: requestId,
    normalized_status: 'failed',
    provider_status: 'error',
    result_urls: [],
    error_code: mapped.code,
    error_message: mapped.message,
    refunded: false,
  };
}

function defaultErrorCodeForStatus(normalizedStatus: NormalizedToolResponse['normalized_status']): string | undefined {
  if (normalizedStatus === 'blocked') {
    return 'REQUEST_BLOCKED_NSFW';
  }

  if (normalizedStatus === 'cancelled') {
    return 'REQUEST_CANCELLED';
  }

  if (normalizedStatus === 'failed') {
    return 'REQUEST_FAILED';
  }

  return undefined;
}
