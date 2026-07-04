import { getDefaultModel, requireAllowedModel } from '../models.js';
import { normalizeRequestRecord, normalizeThrownError } from '../normalize.js';
import { HiggsfieldProviderClient } from '../provider.js';
import type { GenerateImageInput, NormalizedToolResponse } from '../types.js';

export async function generateImage(input: GenerateImageInput): Promise<NormalizedToolResponse> {
  try {
    const model = input.model_id
      ? requireAllowedModel(input.model_id, 'image')
      : getDefaultModel('image');

    const client = new HiggsfieldProviderClient();
    const record = await client.submitImage({
      ...input,
      model_id: model.modelId,
    });

    return normalizeRequestRecord(record);
  } catch (error) {
    return normalizeThrownError(error);
  }
}
