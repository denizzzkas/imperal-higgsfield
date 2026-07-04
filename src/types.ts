export type HiggsfieldTaskType = 'image' | 'video';

export type NormalizedStatus =
  | 'pending'
  | 'running'
  | 'succeeded'
  | 'failed'
  | 'blocked'
  | 'cancelled';

export interface ModelDefinition {
  modelId: string;
  label: string;
  taskType: HiggsfieldTaskType;
  costTier: string;
  recommended: boolean;
  enabled: boolean;
}

export interface GenerateImageInput {
  prompt: string;
  model_id?: string;
  aspect_ratio?: string;
  negative_prompt?: string;
  seed?: number;
}

export interface GenerateVideoInput {
  model_id?: string;
  prompt?: string;
  image_url?: string;
  duration?: number;
  aspect_ratio?: string;
}

export interface RequestStatusInput {
  request_id: string;
}

export interface CancelRequestInput {
  request_id: string;
}

export interface ListModelsInput {
  task_type?: 'image' | 'video' | 'all';
}

export interface NormalizedToolResponse {
  request_id: string;
  normalized_status: NormalizedStatus;
  provider_status: string;
  model_id?: string;
  result_urls?: string[];
  error_code?: string;
  error_message?: string;
  refunded?: boolean;
}

export interface CancelToolResponse {
  request_id: string;
  cancelled: boolean;
  provider_status: string;
}

export interface ListModelsResponse {
  models: Array<{
    model_id: string;
    label: string;
    task_type: HiggsfieldTaskType;
    cost_tier: string;
    recommended: boolean;
  }>;
}

export interface ProviderRequestRecord {
  id: string;
  status: string;
  model?: string;
  output?: string[];
  error?: {
    code?: string;
    message?: string;
  };
}

export interface ProviderImageResponse {
  request_id: string;
  status: string;
  result_url?: string;
  result_urls?: string[];
  detail?: unknown;
}

export interface ProviderVideoResponse {
  request_id: string;
  status: string;
  result_url?: string;
  result_urls?: string[];
  detail?: unknown;
}

export interface ProviderStatusResponse {
  request_id?: string;
  status: string;
  model_id?: string;
  result_url?: string;
  result_urls?: string[];
  detail?: unknown;
}
