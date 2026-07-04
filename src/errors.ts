export type CanonicalErrorCode =
  | 'AUTH_MISSING'
  | 'AUTH_INVALID'
  | 'INSUFFICIENT_PROVIDER_BALANCE'
  | 'RATE_LIMITED'
  | 'MODEL_NOT_FOUND'
  | 'INVALID_INPUT'
  | 'REQUEST_FAILED'
  | 'REQUEST_BLOCKED_NSFW'
  | 'REQUEST_CANCELLED'
  | 'NETWORK_ERROR'
  | 'UNKNOWN_PROVIDER_ERROR';

export class HiggsfieldExtensionError extends Error {
  constructor(
    public readonly code: CanonicalErrorCode,
    message: string,
    public readonly providerStatus?: number,
  ) {
    super(message);
    this.name = 'HiggsfieldExtensionError';
  }
}

export function mapUnknownError(error: unknown): HiggsfieldExtensionError {
  if (error instanceof HiggsfieldExtensionError) {
    return error;
  }

  if (error instanceof Error) {
    return new HiggsfieldExtensionError('UNKNOWN_PROVIDER_ERROR', error.message);
  }

  return new HiggsfieldExtensionError('UNKNOWN_PROVIDER_ERROR', 'Unknown provider error');
}
