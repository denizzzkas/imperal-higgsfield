import { HiggsfieldExtensionError } from './errors.js';

export interface ProviderAuthConfig {
  mode: 'hf_key' | 'key_secret';
  hfKey?: string;
  apiKey?: string;
  apiSecret?: string;
}

export interface AppConfig {
  providerBaseUrl: string;
  auth: ProviderAuthConfig;
}

export function loadConfig(env: Record<string, string | undefined> = process.env): AppConfig {
  const providerBaseUrl = env.HIGGSFIELD_PROVIDER_BASE_URL ?? 'https://platform.higgsfield.ai';
  const mode = env.HIGGSFIELD_PROVIDER_AUTH_MODE as ProviderAuthConfig['mode'] | undefined;

  if (!mode) {
    throw new HiggsfieldExtensionError('AUTH_MISSING', 'Missing HIGGSFIELD_PROVIDER_AUTH_MODE');
  }

  if (mode === 'hf_key') {
    const hfKey = env.HIGGSFIELD_PROVIDER_HF_KEY;
    if (!hfKey) {
      throw new HiggsfieldExtensionError('AUTH_MISSING', 'Missing HIGGSFIELD_PROVIDER_HF_KEY');
    }
    return {
      providerBaseUrl,
      auth: { mode, hfKey },
    };
  }

  if (mode === 'key_secret') {
    const apiKey = env.HIGGSFIELD_PROVIDER_API_KEY;
    const apiSecret = env.HIGGSFIELD_PROVIDER_API_SECRET;
    if (!apiKey || !apiSecret) {
      throw new HiggsfieldExtensionError('AUTH_MISSING', 'Missing HIGGSFIELD_PROVIDER_API_KEY or HIGGSFIELD_PROVIDER_API_SECRET');
    }
    return {
      providerBaseUrl,
      auth: { mode, apiKey, apiSecret },
    };
  }

  throw new HiggsfieldExtensionError('AUTH_INVALID', `Unsupported auth mode: ${String(mode)}`);
}
