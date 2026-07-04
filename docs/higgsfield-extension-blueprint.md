# Higgsfield Extension Blueprint

## 1. Overview

This extension brings Higgsfield Cloud image and video generation into Imperal.

The MVP uses a **managed-only billing model**:

- Imperal owns the Higgsfield Cloud API credentials
- users pay with Imperal tokens
- Imperal absorbs and prices the underlying provider cost

Bring Your Own Key (BYOK) is intentionally postponed until after MVP.

## 2. Confirmed assumptions

### 2.1 Confirmed

- Higgsfield Cloud has a dedicated API surface
- the documented API flow uses Cloud/API credentials
- request execution is asynchronous
- request statuses include:
  - `queued`
  - `in_progress`
  - `completed`
  - `failed`
  - `nsfw`
- failed and `nsfw` requests are documented as refunded
- cancellation is part of the request lifecycle
- cancellation is documented as available only while a request is still `queued`

### 2.2 Not confirmed

The following has **not** been confirmed from official docs:

- that a standard Higgsfield subscription account can be reused directly through API
- that subscriber credits and Cloud API usage share the same billing pool

Therefore MVP must not depend on subscriber-account auth.

## 3. Product decision

### Final MVP decision

Build the extension as an **Imperal-managed provider integration**.

That means:

- no local CLI dependency
- no machine-bound login state
- no assumption that a web subscriber account can call the API
- no user-provided Higgsfield credentials in MVP

## 4. MVP goals

### Primary goals

- generate images through Higgsfield Cloud API
- generate videos from image-based workflows where supported
- expose simple tools to Imperal users
- normalize provider errors and statuses
- support predictable Imperal-side pricing

### Non-goals for MVP

- BYOK support
- local CLI support for end users
- full open-ended provider model discovery
- advanced workflow composition
- webhook infrastructure
- user-owned Higgsfield billing passthrough

## 5. Architecture

### 5.1 Execution model

The extension acts as an orchestration layer:

1. Imperal tool receives a user request
2. tool selects an allowlisted provider model
3. extension submits request to Higgsfield Cloud API
4. extension returns a `request_id`
5. extension polls for lifecycle updates
6. extension returns normalized result URLs on completion

### 5.2 Provider backend

Provider target:

- Higgsfield Cloud API
- base URL: `https://platform.higgsfield.ai`

Provider interaction style:

- asynchronous request submission to `POST /{model_id}`
- status polling by request ID via `GET /requests/{request_id}/status`
- optional cancellation via `POST /requests/{request_id}/cancel`

### 5.3 Authentication model

MVP uses **provider-managed secrets only**.

App-level secret plan:

- `HIGGSFIELD_PROVIDER_AUTH_MODE`
- `HIGGSFIELD_PROVIDER_HF_KEY`
- `HIGGSFIELD_PROVIDER_API_KEY`
- `HIGGSFIELD_PROVIDER_API_SECRET`

The extension should support either:

- single combined key auth
- key + secret auth

depending on which official auth shape is ultimately chosen in implementation.

## 6. Tool surface

The initial tool surface should stay small and stable.

### 6.1 `hf_generate_image`

Purpose:

- submit an image generation request

Inputs:

- `prompt` (required)
- `model_id` (required or defaulted)
- `aspect_ratio` (optional)
- `negative_prompt` (optional)
- `seed` (optional)

Outputs:

- `request_id`
- `normalized_status`
- `provider_status`
- `model_id`
- `result_urls` (if immediately available)

### 6.2 `hf_generate_video`

Purpose:

- submit a video generation request

Inputs:

- `model_id` (required or defaulted)
- `prompt` (optional, depending on model)
- `image_url` (optional, depending on model)
- `duration` (optional)
- `aspect_ratio` (optional)

Outputs:

- `request_id`
- `normalized_status`
- `provider_status`
- `model_id`
- `result_urls` (if available)

### 6.3 `hf_get_request_status`

Purpose:

- inspect a previously submitted request

Inputs:

- `request_id`

Outputs:

- `request_id`
- `normalized_status`
- `provider_status`
- `result_urls` (if completed)
- `error_code` (if failed)
- `error_message` (if present)
- `refunded` (if known)

### 6.4 `hf_cancel_request`

Purpose:

- cancel a running request if provider allows it

Inputs:

- `request_id`

Outputs:

- `request_id`
- `cancelled`
- `provider_status`

### 6.5 `hf_list_models`

Purpose:

- show a curated, app-owned model catalog

Inputs:

- `task_type` = `image | video | all` (optional)

Outputs:

- list of models with:
  - `model_id`
  - `label`
  - `task_type`
  - `cost_tier`
  - `recommended`

## 7. Model strategy

Do not expose the entire provider catalog in MVP.

Use a curated allowlist with pricing tiers.

### 7.1 Initial catalog shape

Suggested internal catalog fields:

- `model_id`
- `label`
- `task_type`
- `supports_image_input`
- `supports_text_input`
- `cost_tier`
- `recommended`
- `enabled`

### 7.2 MVP catalog policy

Start with:

- 2–3 image models
- 1–2 video/image-to-video models
- only models with clear pricing confidence

## 8. Request lifecycle

### 8.1 Submit

Flow:

1. validate tool input
2. resolve default or explicit allowed model
3. build provider request payload
4. submit request to provider
5. store returned `request_id`
6. return normalized response

### 8.2 Poll

Flow:

1. receive `request_id`
2. call provider status endpoint
3. map provider status into normalized status
4. surface result URLs or errors

### 8.3 Cancel

Flow:

1. receive `request_id`
2. call provider cancel endpoint
3. return provider acknowledgement in normalized form

## 9. Status normalization

Provider-to-Imperal status mapping:

- `queued` -> `pending`
- `in_progress` -> `running`
- `completed` -> `succeeded`
- `failed` -> `failed`
- `nsfw` -> `blocked`
- provider cancellation state -> `cancelled`

Normalized response should always include:

- `request_id`
- `normalized_status`
- `provider_status`

## 10. Error model

The extension must normalize provider failures into a stable app-facing set.

### 10.1 Canonical error codes

- `AUTH_MISSING`
- `AUTH_INVALID`
- `INSUFFICIENT_PROVIDER_BALANCE`
- `RATE_LIMITED`
- `MODEL_NOT_FOUND`
- `INVALID_INPUT`
- `REQUEST_FAILED`
- `REQUEST_BLOCKED_NSFW`
- `REQUEST_CANCELLED`
- `NETWORK_ERROR`
- `UNKNOWN_PROVIDER_ERROR`

### 10.2 Error mapping policy

Examples:

- auth failure -> `AUTH_INVALID`
- missing provider secret -> `AUTH_MISSING`
- provider balance/credit issue -> `INSUFFICIENT_PROVIDER_BALANCE`
- validation error -> `INVALID_INPUT`
- unknown provider model -> `MODEL_NOT_FOUND`
- provider-side request failure -> `REQUEST_FAILED`
- NSFW terminal state -> `REQUEST_BLOCKED_NSFW`
- timeout/transport issue -> `NETWORK_ERROR`

## 11. Billing model

### 11.1 MVP billing mode

Only one user-visible billing mode in MVP:

- `managed`

Meaning:

- provider cost is paid by Imperal
- user is charged in Imperal tokens

### 11.2 Pricing strategy

Use **tiered per-action pricing**, not one flat price.

Suggested cost tiers:

- `image_basic`
- `image_pro`
- `video_basic`
- `video_pro`

Pricing must reflect:

- provider request cost
- polling/orchestration overhead
- refund/failed-job behavior where applicable
- safety margin

## 12. Safety and controls

### 12.1 Provider-side risk controls

The app should support:

- model allowlist
- optional per-user usage caps
- premium-model confirmation for expensive video actions
- disabled access to unpriced models

### 12.2 UX defaults

Recommended defaults:

- image generation first-class in MVP
- video generation limited to clearly supported workflows
- conservative default model selection

## 13. User experience

### 13.1 Default usage

A standard user should be able to say:

- generate an image of X
- animate this image
- check status of my generation
- cancel this generation

without needing any separate Higgsfield account setup.

### 13.2 Messaging

The app description should clearly state:

- generation runs through Higgsfield Cloud API
- billing in MVP is managed through Imperal
- personal Higgsfield API account support may come later

## 14. Post-MVP roadmap

### 14.1 BYOK mode

Later addition:

- user-scoped `HF_KEY`
- or `HF_API_KEY` + `HF_API_SECRET`
- explicit user preference for provider billing mode

This mode should use Higgsfield **Cloud API credentials**, not CLI login.

### 14.2 Optional later additions

- broader model catalog
- richer workflow presets
- webhook-based async completion
- cost estimation tool
- prompt presets for recurring use cases

## 15. Recommended repository next steps

1. Create a machine-readable MVP spec (`app.ir.json` draft)
2. Add curated model catalog file
3. Add pricing tier matrix
4. Define secrets schema in extension manifest
5. Implement request/response normalization rules

## 16. Final decision summary

The MVP should be built as a **managed-only Imperal extension over Higgsfield Cloud API**.

Not for MVP:

- local CLI transport
- subscriber-account auth assumptions
- BYOK user mode

Add BYOK only after the managed flow is stable and pricing is proven.
