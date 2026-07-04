import { loadConfig } from './config.js';
import { HiggsfieldExtensionError } from './errors.js';
import type {
  GenerateImageInput,
  GenerateVideoInput,
  ProviderImageResponse,
  ProviderRequestRecord,
  ProviderStatusResponse,
  ProviderVideoResponse,
} from './types.js';

export class HiggsfieldProviderClient {
  private readonly config = loadConfig();

  private buildHeaders(): HeadersInit {
    if (this.config.auth.mode === 'hf_key') {
      return {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${this.config.auth.hfKey}`,
      };
    }

    return {
      'Content-Type': 'application/json',
      'X-API-Key': this.config.auth.apiKey ?? '',
      'X-API-Secret': this.config.auth.apiSecret ?? '',
    };
  }

  async submitImage(input: GenerateImageInput): Promise<ProviderRequestRecord> {
    if (!input.model_id) {
      throw new HiggsfieldExtensionError('INVALID_INPUT', 'Missing model_id for image request');
    }

    const payload = await this.post<ProviderImageResponse>(`/${encodeURIComponent(input.model_id)}`, input);
    return mapImageResponse(payload, input.model_id);
  }

  async submitVideo(input: GenerateVideoInput): Promise<ProviderRequestRecord> {
    if (!input.model_id) {
      throw new HiggsfieldExtensionError('INVALID_INPUT', 'Missing model_id for video request');
    }

    const payload = await this.post<ProviderVideoResponse>(`/${encodeURIComponent(input.model_id)}`, input);
    return mapVideoResponse(payload, input.model_id);
  }

  async getRequest(requestId: string): Promise<ProviderRequestRecord> {
    const payload = await this.get<ProviderStatusResponse>(`/requests/${encodeURIComponent(requestId)}/status`);
    return mapStatusResponse(payload, requestId);
  }

  async cancelRequest(requestId: string): Promise<ProviderRequestRecord> {
    const payload = await this.post<ProviderStatusResponse>(`/requests/${encodeURIComponent(requestId)}/cancel`, {});
    return mapStatusResponse(payload, requestId);
  }

  private async get<T>(path: string): Promise<T> {
    const response = await fetch(`${this.config.providerBaseUrl}${path}`, {
      method: 'GET',
      headers: this.buildHeaders(),
    });

    return this.parseResponse<T>(response);
  }

  private async post<T>(path: string, body: unknown): Promise<T> {
    const response = await fetch(`${this.config.providerBaseUrl}${path}`, {
      method: 'POST',
      headers: this.buildHeaders(),
      body: JSON.stringify(body),
    });

    return this.parseResponse<T>(response);
  }

  private async parseResponse<T>(response: Response): Promise<T> {
    let payload: unknown;

    try {
      payload = await response.json();
    } catch {
      throw new HiggsfieldExtensionError('NETWORK_ERROR', 'Provider returned a non-JSON response', response.status);
    }

    if (!response.ok) {
      throw this.mapProviderHttpError(response.status, payload);
    }

    return payload as T;
  }

  private mapProviderHttpError(status: number, payload: unknown): HiggsfieldExtensionError {
    const message = extractMessage(payload) ?? `Provider request failed with status ${status}`;

    if (status === 401 || status === 403) {
      return new HiggsfieldExtensionError('AUTH_INVALID', message, status);
    }
    if (status === 402) {
      return new HiggsfieldExtensionError('INSUFFICIENT_PROVIDER_BALANCE', message, status);
    }
    if (status === 422 || status === 400) {
      return new HiggsfieldExtensionError('INVALID_INPUT', message, status);
    }
    if (status === 429) {
      return new HiggsfieldExtensionError('RATE_LIMITED', message, status);
    }

    return new HiggsfieldExtensionError('REQUEST_FAILED', message, status);
  }
}

function mapImageResponse(payload: ProviderImageResponse, modelId?: string): ProviderRequestRecord {
  return {
    id: payload.request_id,
    status: payload.status,
    model: modelId,
    output: collectResultUrls(payload),
    error: extractEmbeddedError(payload.detail),
  };
}

function mapVideoResponse(payload: ProviderVideoResponse, modelId?: string): ProviderRequestRecord {
  return {
    id: payload.request_id,
    status: payload.status,
    model: modelId,
    output: collectResultUrls(payload),
    error: extractEmbeddedError(payload.detail),
  };
}

function mapStatusResponse(payload: ProviderStatusResponse, requestId: string): ProviderRequestRecord {
  return {
    id: payload.request_id ?? requestId,
    status: payload.status,
    model: payload.model_id,
    output: collectResultUrls(payload),
    error: extractEmbeddedError(payload.detail),
  };
}

function collectResultUrls(payload: { result_url?: string; result_urls?: string[] }): string[] | undefined {
  const urls = payload.result_urls?.filter((url): url is string => typeof url === 'string' && url.trim().length > 0) ?? [];

  if (urls.length > 0) {
    return urls;
  }

  if (payload.result_url && payload.result_url.trim()) {
    return [payload.result_url];
  }

  return undefined;
}

function extractEmbeddedError(detail: unknown): { code?: string; message?: string } | undefined {
  if (typeof detail === 'string' && detail.trim()) {
    return { message: detail };
  }

  if (detail && typeof detail === 'object') {
    const message = (detail as { message?: unknown; detail?: unknown }).message;
    const fallback = (detail as { detail?: unknown }).detail;
    return {
      message: typeof message === 'string' ? message : typeof fallback === 'string' ? fallback : undefined,
    };
  }

  return undefined;
}

function extractMessage(payload: unknown): string | undefined {
  if (!payload || typeof payload !== 'object') {
    return undefined;
  }

  const maybeMessage = (payload as { message?: unknown; error?: unknown; detail?: unknown }).message;
  if (typeof maybeMessage === 'string' && maybeMessage.trim()) {
    return maybeMessage;
  }

  const maybeDetail = (payload as { detail?: unknown }).detail;
  if (typeof maybeDetail === 'string' && maybeDetail.trim()) {
    return maybeDetail;
  }

  const maybeError = (payload as { error?: unknown }).error;
  if (typeof maybeError === 'string' && maybeError.trim()) {
    return maybeError;
  }

  if (maybeError && typeof maybeError === 'object') {
    const nestedMessage = (maybeError as { message?: unknown }).message;
    if (typeof nestedMessage === 'string' && nestedMessage.trim()) {
      return nestedMessage;
    }
  }

  return undefined;
}
