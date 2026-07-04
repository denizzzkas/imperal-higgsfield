# Request and Response Examples

## Purpose

This file captures normalized request and response examples for the managed-only Higgsfield MVP.

These are app-facing examples, not guaranteed raw provider payloads.

## 1. Generate image

### Tool call

```json
{
  "tool": "hf_generate_image",
  "args": {
    "prompt": "cinematic fashion portrait in Tokyo at night",
    "model_id": "higgsfield-ai/soul/standard",
    "aspect_ratio": "4:5"
  }
}
```

### Initial normalized response

```json
{
  "request_id": "req_12345",
  "normalized_status": "pending",
  "provider_status": "queued",
  "model_id": "higgsfield-ai/soul/standard",
  "result_urls": []
}
```

Provider path example:

`POST https://platform.higgsfield.ai/higgsfield-ai/soul/standard`

## 2. Generate video from image

### Tool call

```json
{
  "tool": "hf_generate_video",
  "args": {
    "model_id": "bytedance/seedance/v1/pro/image-to-video",
    "image_url": "https://example.com/source.png",
    "prompt": "subtle cinematic camera move",
    "duration": 5
  }
}
```

### Initial normalized response

```json
{
  "request_id": "req_67890",
  "normalized_status": "pending",
  "provider_status": "queued",
  "model_id": "bytedance/seedance/v1/pro/image-to-video",
  "result_urls": []
}
```

Provider path example:

`POST https://platform.higgsfield.ai/bytedance%2Fseedance%2Fv1%2Fpro%2Fimage-to-video`

## 3. Poll request status while running

### Tool call

```json
{
  "tool": "hf_get_request_status",
  "args": {
    "request_id": "req_67890"
  }
}
```

### Running response

```json
{
  "request_id": "req_67890",
  "normalized_status": "running",
  "provider_status": "in_progress",
  "result_urls": []
}
```

## 4. Poll request status on completion

### Completed response

```json
{
  "request_id": "req_67890",
  "normalized_status": "succeeded",
  "provider_status": "completed",
  "result_urls": [
    "https://example.com/output/video.mp4"
  ]
}
```

## 5. Failed request

### Failed response

```json
{
  "request_id": "req_fail_1",
  "normalized_status": "failed",
  "provider_status": "failed",
  "error_code": "REQUEST_FAILED",
  "error_message": "Provider returned a terminal failed state.",
  "refunded": true,
  "result_urls": []
}
```

## 6. NSFW-blocked request

### Blocked response

```json
{
  "request_id": "req_nsfw_1",
  "normalized_status": "blocked",
  "provider_status": "nsfw",
  "error_code": "REQUEST_BLOCKED_NSFW",
  "error_message": "Request was blocked by provider safety checks.",
  "refunded": true,
  "result_urls": []
}
```

Status polling path example:

`GET https://platform.higgsfield.ai/requests/req_67890/status`

## 7. Cancel request

### Tool call

```json
{
  "tool": "hf_cancel_request",
  "args": {
    "request_id": "req_67890"
  }
}
```

### Cancel response

```json
{
  "request_id": "req_67890",
  "cancelled": true,
  "provider_status": "cancelled"
}
```

Provider path example:

`POST https://platform.higgsfield.ai/requests/req_67890/cancel`

Note: Higgsfield docs say cancellation is available only while the request is still `queued`.

## 8. List models

### Tool call

```json
{
  "tool": "hf_list_models",
  "args": {
    "task_type": "all"
  }
}
```

### Response

```json
{
  "models": [
    {
      "model_id": "reve/text-to-image",
      "label": "Fast Image",
      "task_type": "image",
      "cost_tier": "image_basic",
      "recommended": true
    },
    {
      "model_id": "higgsfield-ai/soul/standard",
      "label": "Higgsfield Soul",
      "task_type": "image",
      "cost_tier": "image_pro",
      "recommended": true
    },
    {
      "model_id": "bytedance/seedance/v1/pro/image-to-video",
      "label": "Seedance Image to Video",
      "task_type": "video",
      "cost_tier": "video_pro",
      "recommended": true
    }
  ]
}
```
