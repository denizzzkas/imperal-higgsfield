# Secrets and Configuration

## Purpose

This file defines the managed-mode secrets and configuration surface for the Higgsfield Imperal MVP.

The MVP does not support user-provided Higgsfield credentials.

## Secrets scope

MVP uses **app-level secrets only**.

These secrets belong to the extension/operator side and are used for all managed requests.

## Required secret plan

### 1) `HIGGSFIELD_PROVIDER_AUTH_MODE`

Controls which auth shape the integration should use.

Allowed values:
- `hf_key`
- `api_key_secret`

### 2) `HIGGSFIELD_PROVIDER_HF_KEY`

Used when auth mode is:
- `hf_key`

Meaning:
- a single provider credential value used to call Higgsfield Cloud API

### 3) `HIGGSFIELD_PROVIDER_API_KEY`

Used when auth mode is:
- `key_secret`

Meaning:
- provider API key

### 4) `HIGGSFIELD_PROVIDER_API_SECRET`

Used when auth mode is:
- `key_secret`

Meaning:
- provider API secret

## Secret validation rules

The extension should validate secrets before sending provider requests.

### If `HIGGSFIELD_PROVIDER_AUTH_MODE = hf_key`
Required:
- `HIGGSFIELD_PROVIDER_HF_KEY`

If missing:
- return normalized error `AUTH_MISSING`

### If `HIGGSFIELD_PROVIDER_AUTH_MODE = api_key_secret`
Required:
- `HIGGSFIELD_PROVIDER_API_KEY`
- `HIGGSFIELD_PROVIDER_API_SECRET`

If either is missing:
- return normalized error `AUTH_MISSING`

### If auth mode is unknown
Return:
- `AUTH_INVALID`
- or configuration validation failure during setup, depending on final runtime shape

## Runtime configuration

These values are not necessarily secrets, but should be treated as controlled app configuration.

### Recommended config keys

- `DEFAULT_IMAGE_MODEL_ID`
- `DEFAULT_VIDEO_MODEL_ID`
- `ENABLE_VIDEO_MVP`
- `PREMIUM_VIDEO_CONFIRMATION_REQUIRED`
- `MODEL_ALLOWLIST_VERSION`

## Model defaults

Suggested initial defaults:

- `DEFAULT_IMAGE_MODEL_ID = reve/text-to-image`
- `DEFAULT_VIDEO_MODEL_ID = bytedance/seedance/v1/pro/image-to-video`

These defaults should always point to enabled allowlisted models.

## Future post-MVP additions

When BYOK is introduced later, it should use **user-scoped secrets**, not app-scoped ones.

Deferred user secret plan:
- `HF_KEY`
- or `HF_API_KEY`
- `HF_API_SECRET`

That mode is intentionally out of scope for MVP.
