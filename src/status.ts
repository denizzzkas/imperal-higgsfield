import type { NormalizedStatus } from './types.js';

const STATUS_MAP: Record<string, NormalizedStatus> = {
  queued: 'pending',
  pending: 'pending',
  in_progress: 'running',
  processing: 'running',
  completed: 'succeeded',
  succeeded: 'succeeded',
  failed: 'failed',
  nsfw: 'blocked',
  blocked: 'blocked',
  cancelled: 'cancelled',
  canceled: 'cancelled',
};

export function normalizeStatus(providerStatus: string): NormalizedStatus {
  return STATUS_MAP[providerStatus] ?? 'failed';
}
