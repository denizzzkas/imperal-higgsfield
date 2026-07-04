import { getDefaultModel, requireAllowedModel } from '../models.js';
import { normalizeRequestRecord, normalizeThrownError } from '../normalize.js';
import { HiggsfieldProviderClient } from '../provider.js';
import type { GenerateVideoInput, NormalizedToolResponse } from '../types.js';

export async function generateVideo(input: GenerateVideoInput): Promise<NormalizedToolResponse> {
  try {
    const model = input.model_id
      ? requireAllowedModel(input.model_id, 'video')
      : getDefaultModel('video');

    const client = new HiggsfieldProviderClient();
    const record = await client.submitVideo({
      ...input,
      model_id: model.modelId,
    });

    return normalizeRequestRecord(record);
  } catch (error) {
    return normalizeThrownError(error);
  }
}
