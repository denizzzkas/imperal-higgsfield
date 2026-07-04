# Pricing Matrix

## Purpose

This file defines the first pricing structure for the managed-only Higgsfield MVP.

The exact Imperal token values are placeholders until real provider cost data is validated.

## Pricing principles

- users pay in Imperal tokens only
- Higgsfield Cloud API cost is absorbed by Imperal in MVP
- prices must be tiered by workload class
- video must never be priced like image generation
- only allowlisted models should be exposed until margins are proven

## Billing mode in MVP

- `managed`

No BYOK pricing is needed in MVP.

## Cost tiers

### `image_basic`

Use for:
- fast general image generation
- lower-cost text-to-image models

Suggested placeholder range:
- 300–600 Imperal tokens per generation

Example model candidates:
- `reve/text-to-image`

### `image_pro`

Use for:
- premium quality image generation
- portrait or stylized models with higher provider cost

Suggested placeholder range:
- 700–1200 Imperal tokens per generation

Example model candidates:
- `higgsfield-ai/soul/standard`

### `video_basic`

Use for:
- lower-cost short video generation workflows
- only if provider costs are predictable enough

Suggested placeholder range:
- 1500–3000 Imperal tokens per generation

### `video_pro`

Use for:
- premium image-to-video or cinematic video generation
- models with clearly higher provider cost

Suggested placeholder range:
- 3000+ Imperal tokens per generation

Example model candidates:
- `bytedance/seedance/v1/pro/image-to-video`

## Inputs that can affect future pricing

These are not part of MVP pricing logic yet, but should be documented for later:

- model family
- resolution
- aspect ratio
- duration
- number of outputs
- queue priority

## Recommended MVP policy

For the first release:

- keep pricing fixed per model tier
- do not expose user-adjustable quality ladders unless cost is known
- keep premium video models on a short allowlist
- optionally require confirmation before expensive video actions

## Future evolution

Possible post-MVP pricing improvements:

- dynamic pricing by duration or output count
- reduced orchestration fee for BYOK mode
- separate pricing for retries or premium priority
