# Model Catalog

## Purpose

This file tracks the curated provider models that the Higgsfield Imperal extension is allowed to expose in MVP.

MVP should use a strict allowlist rather than open provider discovery.

## Catalog policy

A model can be enabled only if:

- its task type is clearly understood
- the request shape is documented well enough to implement safely
- the likely provider cost fits a known pricing tier
- the result format can be normalized cleanly

## Catalog fields

Each model entry should track:

- `model_id`
- `label`
- `task_type`
- `supports_text_input`
- `supports_image_input`
- `cost_tier`
- `recommended`
- `enabled`
- `notes`

## MVP allowlist draft

### 1) Fast Image

- `model_id`: `reve/text-to-image`
- `label`: `Fast Image`
- `task_type`: `image`
- `supports_text_input`: `true`
- `supports_image_input`: `false`
- `cost_tier`: `image_basic`
- `recommended`: `true`
- `enabled`: `true`
- `notes`: Good candidate for default general text-to-image flow.

### 2) Higgsfield Soul

- `model_id`: `higgsfield-ai/soul/standard`
- `label`: `Higgsfield Soul`
- `task_type`: `image`
- `supports_text_input`: `true`
- `supports_image_input`: `false`
- `cost_tier`: `image_pro`
- `recommended`: `true`
- `enabled`: `true`
- `notes`: Premium image tier candidate.

### 3) Higgsfield Dop

- `model_id`: `higgsfield-ai/dop/preview`
- `label`: `Higgsfield Dop`
- `task_type`: `video`
- `supports_text_input`: `false`
- `supports_image_input`: `true`
- `cost_tier`: `video_basic`
- `recommended`: `false`
- `enabled`: `true`
- `notes`: Mentioned in the video guide as a popular image-to-video model.

### 4) Seedance Image to Video

- `model_id`: `bytedance/seedance/v1/pro/image-to-video`
- `label`: `Seedance Image to Video`
- `task_type`: `video`
- `supports_text_input`: `false`
- `supports_image_input`: `true`
- `cost_tier`: `video_pro`
- `recommended`: `true`
- `enabled`: `true`
- `notes`: Strong candidate for initial image-to-video flow.

### 5) Kling 2.1 Image to Video

- `model_id`: `kling-video/v2.1/pro/image-to-video`
- `label`: `Kling 2.1 Image to Video`
- `task_type`: `video`
- `supports_text_input`: `false`
- `supports_image_input`: `true`
- `cost_tier`: `video_pro`
- `recommended`: `false`
- `enabled`: `true`
- `notes`: Listed in the official video guide as an advanced cinematic image-to-video option.

## Deferred models

These should stay disabled until implementation and pricing are clearer:

- additional cinematic video models
- text-to-video models with uncertain request format
- any model with unclear billing behavior
- any model whose output normalization is inconsistent

## Future additions

Post-MVP, this file can evolve into a machine-readable catalog source if needed.
