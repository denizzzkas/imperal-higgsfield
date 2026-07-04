import { HiggsfieldExtensionError } from './errors.js';
import type { HiggsfieldTaskType, ModelDefinition } from './types.js';

export const MODELS: ModelDefinition[] = [
  {
    modelId: 'reve/text-to-image',
    label: 'Fast Image',
    taskType: 'image',
    costTier: 'image_basic',
    recommended: true,
    enabled: true,
  },
  {
    modelId: 'higgsfield-ai/soul/standard',
    label: 'Higgsfield Soul',
    taskType: 'image',
    costTier: 'image_pro',
    recommended: true,
    enabled: true,
  },
  {
    modelId: 'higgsfield-ai/dop/preview',
    label: 'Higgsfield Dop',
    taskType: 'video',
    costTier: 'video_basic',
    recommended: false,
    enabled: true,
  },
  {
    modelId: 'bytedance/seedance/v1/pro/image-to-video',
    label: 'Seedance Image to Video',
    taskType: 'video',
    costTier: 'video_pro',
    recommended: true,
    enabled: true,
  },
  {
    modelId: 'kling-video/v2.1/pro/image-to-video',
    label: 'Kling 2.1 Image to Video',
    taskType: 'video',
    costTier: 'video_pro',
    recommended: false,
    enabled: true,
  },
];

export function listModels(taskType: HiggsfieldTaskType | 'all' = 'all'): ModelDefinition[] {
  return MODELS.filter((model) => model.enabled && (taskType === 'all' || model.taskType === taskType));
}

export function getDefaultModel(taskType: HiggsfieldTaskType): ModelDefinition {
  const model = MODELS.find((item) => item.taskType === taskType && item.recommended && item.enabled);
  if (!model) {
    throw new HiggsfieldExtensionError('REQUEST_FAILED', `No enabled default model for task type: ${taskType}`);
  }
  return model;
}

export function requireAllowedModel(modelId: string, taskType: HiggsfieldTaskType): ModelDefinition {
  const model = MODELS.find((item) => item.modelId === modelId && item.taskType === taskType && item.enabled);
  if (!model) {
    throw new HiggsfieldExtensionError('MODEL_NOT_FOUND', `Model not allowed: ${modelId}`);
  }
  return model;
}
