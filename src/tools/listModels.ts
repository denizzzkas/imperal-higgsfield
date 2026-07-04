import { listModels as listModelsCatalog } from '../models.js';
import type { ListModelsInput, ListModelsResponse } from '../types.js';

export async function listModels(input: ListModelsInput = {}): Promise<ListModelsResponse> {
  const taskType = input.task_type ?? 'all';
  return {
    models: listModelsCatalog(taskType).map((model) => ({
      model_id: model.modelId,
      label: model.label,
      task_type: model.taskType,
      cost_tier: model.costTier,
      recommended: model.recommended,
    })),
  };
}
