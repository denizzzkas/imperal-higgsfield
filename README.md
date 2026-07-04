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

## Current tool surface

### 1. `hf_generate_image`
Creates an image generation request.

Input fields:
- `prompt` — required
- `model_id` — optional, defaulted from curated catalog
- `aspect_ratio` — optional
- `negative_prompt` — optional
- `seed` — optional

Flow:
- handler validates or defaults `model_id`
- handler calls `HiggsfieldProviderClient.submit_image(...)`
- client sends `POST {base_url}/{urlencoded_model_id}`
- current default base URL is `https://platform.higgsfield.ai`

Concrete code path:
- tool: `main.py -> hf_generate_image`
- handler: `handlers/generate_image.py`
- client call: `clients/higgsfield_client.py::submit_image`

Concrete provider path shape:
- `POST /reve%2Ftext-to-image`
- `POST /higgsfield-ai%2Fsoul%2Fstandard`

### 2. `hf_generate_video`
Creates a video generation request.

Input fields:
- `model_id` — optional, defaulted from curated catalog
- `prompt` — optional
- `image_url` — optional
- `duration` — optional
- `aspect_ratio` — optional

Validation:
- at least one of `prompt` or `image_url` must be provided

Flow:
- handler validates or defaults `model_id`
- handler calls `HiggsfieldProviderClient.submit_video(...)`
- client sends `POST {base_url}/{model_id}`

Concrete code path:
- tool: `main.py -> hf_generate_video`
- handler: `handlers/generate_video.py`
- client call: `clients/higgsfield_client.py::submit_video`

Concrete provider path shape:
- `POST /higgsfield-ai/dop/preview`
- `POST /bytedance/seedance/v1/pro/image-to-video`
- `POST /kling-video/v2.1/pro/image-to-video`

### 3. `hf_get_request_status`
Checks an existing request.

Input fields:
- `request_id` — required

Flow:
- handler calls `HiggsfieldProviderClient.get_request(...)`
- client sends `GET {base_url}/requests/{request_id}/status`
- provider status is normalized by `core/status.py`

Concrete code path:
- tool: `main.py -> hf_get_request_status`
- handler: `handlers/get_request_status.py`
- client call: `clients/higgsfield_client.py::get_request`

Concrete provider path:
- `GET /requests/{request_id}/status`

### 4. `hf_cancel_request`
Attempts to cancel an existing request.

Input fields:
- `request_id` — required

Flow:
- handler calls `HiggsfieldProviderClient.cancel_request(...)`
- client sends `POST {base_url}/requests/{request_id}/cancel`

Concrete code path:
- tool: `main.py -> hf_cancel_request`
- handler: `handlers/cancel_request.py`
- client call: `clients/higgsfield_client.py::cancel_request`

Concrete provider path:
- `POST /requests/{request_id}/cancel`

### 5. `hf_list_models`
Returns the curated model catalog from the extension itself.

Input fields:
- `task_type` — `image`, `video`, or `all`

Flow:
- no Higgsfield API call is made here
- response is built from `core/models_catalog.py`

Concrete code path:
- tool: `main.py -> hf_list_models`
- handler: `handlers/list_models.py`
- catalog source: `core/models_catalog.py`

## Current allowlisted models

Image:
- `reve/text-to-image`
- `higgsfield-ai/soul/standard`

Video:
- `higgsfield-ai/dop/preview`
- `bytedance/seedance/v1/pro/image-to-video`
- `kling-video/v2.1/pro/image-to-video`

## Auth and config

Secrets used by the extension:
- `HIGGSFIELD_PROVIDER_AUTH_MODE` — currently supported in code as `hf_key` or `api_key_secret`
- `HIGGSFIELD_PROVIDER_HF_KEY`
- `HIGGSFIELD_PROVIDER_API_KEY`
- `HIGGSFIELD_PROVIDER_API_SECRET`

Optional env/config:
- `HIGGSFIELD_PROVIDER_BASE_URL`
  - default in code: `https://platform.higgsfield.ai`

Auth header behavior:

### `hf_key` mode
Sends:
- `Authorization: Bearer <HIGGSFIELD_PROVIDER_HF_KEY>`
- `Content-Type: application/json`

### `api_key_secret` mode
Sends:
- `X-API-Key: <HIGGSFIELD_PROVIDER_API_KEY>`
- `X-API-Secret: <HIGGSFIELD_PROVIDER_API_SECRET>`
- `Content-Type: application/json`

## Important implementation note about provider paths

The extension is now aligned with the currently readable official Higgsfield docs:
- `https://docs.higgsfield.ai/docs/how-to/introduction`
- `https://docs.higgsfield.ai/docs/guides/images`
- `https://docs.higgsfield.ai/docs/guides/video`
- `https://docs.higgsfield.ai/docs/how-to/sdk`
- `https://docs.higgsfield.ai/docs/how-to/webhooks`

Confirmed from docs:
- base URL: `https://platform.higgsfield.ai`
- submit endpoint: `POST /{model_id}`
- status endpoint: `GET /requests/{request_id}/status`
- cancel endpoint: `POST /requests/{request_id}/cancel`
- async statuses include: `queued`, `in_progress`, `completed`, `failed`, `nsfw`
- webhooks are supported through `hf_webhook` query parameter on generation requests
- authentication supports either a single key or an API key + secret

That shape is wired concretely in:
- `clients/higgsfield_client.py`

So yes: the extension already has concrete HTTP calls and concrete paths, and those paths match the readable official docs pages.

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

## What currently does not call Higgsfield dynamically

`hf_list_models` does not fetch models from Higgsfield. It returns the app-owned curated allowlist.

That is intentional for MVP stability.

## Concrete tool surface and provider calls

### `hf_generate_image`
- registered in `main.py`
- handler: `handlers/generate_image.py`
- client method: `HiggsfieldProviderClient.submit_image()`
- HTTP call: `POST {base_url}/{urlencoded_model_id}`
- current base URL default: `https://platform.higgsfield.ai`
- example real path:
  - `POST https://platform.higgsfield.ai/higgsfield-ai%2Fsoul%2Fstandard`

### `hf_generate_video`
- registered in `main.py`
- handler: `handlers/generate_video.py`
- client method: `HiggsfieldProviderClient.submit_video()`
- HTTP call: `POST {base_url}/{urlencoded_model_id}`
- example real path:
  - `POST https://platform.higgsfield.ai/bytedance%2Fseedance%2Fv1%2Fpro%2Fimage-to-video`

### `hf_get_request_status`
- registered in `main.py`
- handler: `handlers/get_request_status.py`
- client method: `HiggsfieldProviderClient.get_request()`
- HTTP call:
  - `GET https://platform.higgsfield.ai/requests/{request_id}/status`

### `hf_cancel_request`
- registered in `main.py`
- handler: `handlers/cancel_request.py`
- client method: `HiggsfieldProviderClient.cancel_request()`
- HTTP call:
  - `POST https://platform.higgsfield.ai/requests/{request_id}/cancel`

### `hf_list_models`
- registered in `main.py`
- handler: `handlers/list_models.py`
- does **not** call Higgsfield API
- returns the curated allowlist from `core/models_catalog.py`

## Current curated models

Image:
- `reve/text-to-image`
- `higgsfield-ai/soul/standard`

Video:
- `higgsfield-ai/dop/preview`
- `bytedance/seedance/v1/pro/image-to-video`
- `kling-video/v2.1/pro/image-to-video`

## Auth modes implemented in code

### `hf_key`
Headers sent:
- `Authorization: Bearer <HIGGSFIELD_PROVIDER_HF_KEY>`
- `Content-Type: application/json`

### `api_key_secret`
Headers sent:
- `X-API-Key: <HIGGSFIELD_PROVIDER_API_KEY>`
- `X-API-Secret: <HIGGSFIELD_PROVIDER_API_SECRET>`
- `Content-Type: application/json`

## Important note about Higgsfield docs alignment

I verified the extension routes against the readable official docs pages:
- `https://docs.higgsfield.ai/docs/how-to/introduction`
- `https://docs.higgsfield.ai/docs/guides/images`
- `https://docs.higgsfield.ai/docs/guides/video`
- `https://docs.higgsfield.ai/docs/how-to/sdk`
- `https://docs.higgsfield.ai/docs/how-to/webhooks`

Confirmed from docs:
- base URL is `https://platform.higgsfield.ai`
- generation requests go to `POST /{model_id}`
- request status is `GET /requests/{request_id}/status`
- cancel is `POST /requests/{request_id}/cancel`
- image docs mention `higgsfield-ai/soul/standard` and `reve/text-to-image`
- video docs mention `higgsfield-ai/dop/preview`, `bytedance/seedance/v1/pro/image-to-video`, and `kling-video/v2.1/pro/image-to-video`
- docs confirm async queue statuses including `queued`, `in_progress`, `completed`, `failed`, and `nsfw`
- docs confirm webhook support via `hf_webhook` query parameter on generation requests
- docs confirm authentication can use either a single key or an API key + secret

This means the extension already uses explicit HTTP methods and explicit paths that match the readable official docs — not abstract placeholders.

What I have verified in code:
- image submit path is URL-encoded correctly
- video submit path is URL-encoded correctly
- request status path is explicit
- cancel path is explicit
- auth headers are explicit
- model list is local/curated, but the current allowlist matches models mentioned in docs

## Local checks

```bash
pytest -q
python3 -m py_compile app.py main.py clients/higgsfield_client.py core/config.py core/errors.py core/models_catalog.py core/normalize.py core/status.py handlers/*.py models/*.py tests/*.py
```
