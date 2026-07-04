import { cancelRequest } from './tools/cancelRequest.js';
import { generateImage } from './tools/generateImage.js';
import { getRequestStatus } from './tools/getRequestStatus.js';
import { listModels } from './tools/listModels.js';

function jsonResponse(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

const originalFetch = globalThis.fetch;

globalThis.fetch = async (input: string | URL | Request, init?: RequestInit): Promise<Response> => {
  const url = typeof input === 'string' ? input : input instanceof URL ? input.toString() : input.url;
  const method = init?.method ?? (input instanceof Request ? input.method : 'GET');

  if (method === 'POST' && url.endsWith('/reve%2Ftext-to-image')) {
    return jsonResponse({
      request_id: 'req_img_1',
      status: 'queued',
      result_urls: [],
    });
  }

  if (method === 'GET' && url.endsWith('/requests/req_done/status')) {
    return jsonResponse({
      request_id: 'req_done',
      status: 'completed',
      model_id: 'reve/text-to-image',
      result_urls: ['https://example.com/result-1.png', 'https://example.com/result-2.png'],
    });
  }

  if (method === 'POST' && url.endsWith('/requests/req_cancel/cancel')) {
    return jsonResponse({
      request_id: 'req_cancel',
      status: 'cancelled',
    });
  }

  if (method === 'GET' && url.endsWith('/requests/req_missing/status')) {
    return jsonResponse({ detail: 'Request not found' }, 404);
  }

  return jsonResponse({ detail: `Unhandled mock route: ${method} ${url}` }, 500);
};

process.env.HIGGSFIELD_PROVIDER_AUTH_MODE = 'hf_key';
process.env.HIGGSFIELD_PROVIDER_HF_KEY = 'test-key';
process.env.HIGGSFIELD_PROVIDER_BASE_URL = 'https://platform.higgsfield.ai';

async function main(): Promise<void> {
  console.log('listModels', await listModels({ task_type: 'all' }));
  console.log('generateImage', await generateImage({ prompt: 'test image' }));
  console.log('getRequestStatus:succeeded', await getRequestStatus({ request_id: 'req_done' }));
  console.log('getRequestStatus:failed', await getRequestStatus({ request_id: 'req_missing' }));
  console.log('cancelRequest', await cancelRequest({ request_id: 'req_cancel' }));
}

main()
  .catch((error) => {
    console.error(error);
    process.exitCode = 1;
  })
  .finally(() => {
    globalThis.fetch = originalFetch;
  });
