# Imperal Higgsfield Extension

Native Python Imperal extension for Higgsfield image and video generation.

## Structure

- `app.py` — runtime entrypoint
- `main.py` — extension wiring, secrets and tool registration
- `clients/` — Higgsfield API client
- `core/` — config, errors, status and normalization
- `handlers/` — tool handlers
- `models/` — pydantic input/output models
- `requirements.txt` — Python dependencies
- `imperal.json` / `manifest.json` — extension metadata

## Tool surface

### `hf_generate_image`
Creates an image generation request.

Input:
- `prompt` — required
- `model_id` — optional, defaulted from curated catalog
- `aspect_ratio` — optional
- `negative_prompt` — optional
- `seed` — optional

Flow:
- tool: `main.py -> hf_generate_image`
- handler: `handlers/generate_image.py`
- client call: `clients/higgsfield_client.py::submit_image`
- HTTP: `POST {base_url}/{urlencoded_model_id}`

Examples:
- `POST /reve%2Ftext-to-image`
- `POST /higgsfield-ai%2Fsoul%2Fstandard`

### `hf_generate_video`
Creates a video generation request.

Input:
- `model_id` — optional, defaulted from curated catalog
- `prompt` — optional
- `image_url` — optional
- `duration` — optional
- `aspect_ratio` — optional

Validation:
- at least one of `prompt` or `image_url` must be provided

Flow:
- tool: `main.py -> hf_generate_video`
- handler: `handlers/generate_video.py`
- client call: `clients/higgsfield_client.py::submit_video`
- HTTP: `POST {base_url}/{urlencoded_model_id}`

Examples:
- `POST /higgsfield-ai%2Fdop%2Fpreview`
- `POST /bytedance%2Fseedance%2Fv1%2Fpro%2Fimage-to-video`
- `POST /kling-video%2Fv2.1%2Fpro%2Fimage-to-video`

### `hf_get_request_status`
Checks an existing request.

Input:
- `request_id` — required

Flow:
- tool: `main.py -> hf_get_request_status`
- handler: `handlers/get_request_status.py`
- client call: `clients/higgsfield_client.py::get_request`
- HTTP: `GET {base_url}/requests/{request_id}/status`

### `hf_cancel_request`
Attempts to cancel an existing request.

Input:
- `request_id` — required

Flow:
- tool: `main.py -> hf_cancel_request`
- handler: `handlers/cancel_request.py`
- client call: `clients/higgsfield_client.py::cancel_request`
- HTTP: `POST {base_url}/requests/{request_id}/cancel`

### `hf_list_models`
Returns the curated model catalog from the extension itself.

Input:
- `task_type` — `image`, `video`, or `all`

Flow:
- tool: `main.py -> hf_list_models`
- handler: `handlers/list_models.py`
- source: `core/models_catalog.py`
- no Higgsfield API call is made

## Current curated models

Image:
- `reve/text-to-image`
- `higgsfield-ai/soul/standard`

Video:
- `higgsfield-ai/dop/preview`
- `bytedance/seedance/v1/pro/image-to-video`
- `kling-video/v2.1/pro/image-to-video`

## Auth and config

Secrets:
- `HIGGSFIELD_PROVIDER_AUTH_MODE` — `hf_key` or `api_key_secret`
- `HIGGSFIELD_PROVIDER_HF_KEY`
- `HIGGSFIELD_PROVIDER_API_KEY`
- `HIGGSFIELD_PROVIDER_API_SECRET`

Optional config:
- `HIGGSFIELD_PROVIDER_BASE_URL`
  - default: `https://platform.higgsfield.ai`

### `hf_key` mode
Headers:
- `Authorization: Bearer <HIGGSFIELD_PROVIDER_HF_KEY>`
- `Content-Type: application/json`

### `api_key_secret` mode
Headers:
- `X-API-Key: <HIGGSFIELD_PROVIDER_API_KEY>`
- `X-API-Secret: <HIGGSFIELD_PROVIDER_API_SECRET>`
- `Content-Type: application/json`

## Docs alignment

Verified against readable official docs:
- `https://docs.higgsfield.ai/docs/how-to/introduction`
- `https://docs.higgsfield.ai/docs/guides/images`
- `https://docs.higgsfield.ai/docs/guides/video`
- `https://docs.higgsfield.ai/docs/how-to/sdk`
- `https://docs.higgsfield.ai/docs/how-to/webhooks`

Confirmed from docs:
- base URL: `https://platform.higgsfield.ai`
- generation endpoint: `POST /{model_id}`
- status endpoint: `GET /requests/{request_id}/status`
- cancel endpoint: `POST /requests/{request_id}/cancel`
- async statuses include `queued`, `in_progress`, `completed`, `failed`, `nsfw`
- webhooks are supported via `hf_webhook`
- auth supports either a single key or API key + secret

## Status normalization

Provider -> normalized:
- `queued` -> `pending`
- `pending` -> `pending`
- `in_progress` -> `running`
- `processing` -> `running`
- `completed` -> `succeeded`
- `succeeded` -> `succeeded`
- `failed` -> `failed`
- `nsfw` -> `blocked`
- `blocked` -> `blocked`
- `cancelled` -> `cancelled`
- `canceled` -> `cancelled`

Implemented in:
- `core/status.py`

## Local checks

```bash
pytest -q
python3 -m py_compile app.py main.py clients/higgsfield_client.py core/config.py core/errors.py core/models_catalog.py core/normalize.py core/status.py handlers/*.py models/*.py tests/*.py
```
