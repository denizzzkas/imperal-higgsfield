# Implementation Plan

## Purpose

This file breaks the managed-only Higgsfield Imperal extension into practical implementation phases.

## Important reality check

Right now this repository contains:
- product docs
- a draft `app.ir.json`

It does **not** yet contain a real runtime implementation of the extension.

That means actual code starts after the spec surface is stable enough to turn into handlers/runtime logic.

## What counts as “writing the extension code” here

Real implementation begins when we add one of these:

1. a real Imperal-compatible IR schema and deployable manifest
2. executable handler code that can:
   - receive tool input
   - resolve auth
   - call Higgsfield endpoints
   - normalize output
3. tests or smoke scripts against known provider payload shapes

Until then, we are still in the specification stage.

## Recommended build sequence

### Phase 1 — Freeze the MVP contract

Goal:
- stop changing core product assumptions every hour

Deliverables:
- `docs/higgsfield-extension-blueprint.md`
- `docs/mvp-scope.md`
- `docs/pricing-matrix.md`
- `docs/model-catalog.md`
- `docs/request-response-examples.md`
- `docs/secrets-and-config.md`

Exit condition:
- we agree that MVP is managed-only
- the 5-tool surface is accepted
- the normalized status/error model is accepted

### Phase 2 — Replace draft IR with real Imperal IR

Goal:
- convert `app.ir.json` into a format that Imperal can actually deploy

Deliverables:
- real app metadata structure
- real tool declarations in the required schema
- declared secrets in the required schema
- pricing skeleton in the required schema

Blocking dependency:
- a real Imperal IR example or schema reference

Exit condition:
- `app.ir.json` validates against the real platform shape

### Phase 3 — Implement provider request logic

Goal:
- add executable code for request orchestration

Likely implementation pieces:
- auth resolver
- model resolver
- request payload builder
- status mapper
- error mapper
- cancel handler

Expected functions:
- `generateImage()`
- `generateVideo()`
- `getRequestStatus()`
- `cancelRequest()`
- `listModels()`

Exit condition:
- handlers can call the provider with known payloads and return normalized app-facing responses

### Phase 4 — Add smoke tests and fixture-based verification

Goal:
- make sure the extension behaves predictably before deploy

Deliverables:
- request fixtures
- example provider responses
- normalized output snapshots
- auth/config validation checks

Exit condition:
- each tool has at least one success example and one failure example covered

### Phase 5 — Deploy in dev mode

Goal:
- install and smoke the extension in Imperal developer flow

Deliverables:
- deployable app package
- secrets saved in dev environment
- smoke runs for all 5 tools

Exit condition:
- the extension can be invoked from Imperal and return normalized results

## What is missing before code can be written confidently

### Missing item 1: real Imperal runtime shape

We still do not know the exact deployable schema for:
- app manifest/IR
- HTTP action declarations
- secrets declarations
- pricing declarations

### Missing item 2: confirmed Higgsfield endpoint contract

We still need the exact provider contract for:
- auth headers
- submit endpoints
- status endpoint shape
- cancel endpoint shape
- result payload structure

### Missing item 3: chosen implementation runtime

We need to know whether this extension should be implemented as:
- pure declarative IR
- IR + remote HTTP integration
- a git-backed app with actual source code

## Honest answer to “when do you start writing code?”

The answer is:

- **spec work is already done enough to start the next stage**
- **real extension code starts as soon as we have either**:
  1. a real Imperal IR schema/example, or
  2. a decision to build a git-backed app with source code

So the practical boundary is:
- **right now we are at the edge of implementation**
- **the next useful coding step is to create actual runtime files, not more concept docs**

## Best next move

I recommend the next implementation step to be one of these:

### Option A — Build a git-backed app scaffold

Create actual source files, for example:
- `src/` or `handlers/`
- request/response normalization code
- provider client skeleton
- config loader

This is the fastest path if we do not yet have a real Imperal IR schema.

### Option B — Research the real Imperal IR shape first

Use Imperal developer docs or a known working app example, then reshape `app.ir.json` properly before writing runtime code.

This is the safest path if deployment format matters immediately.

## Recommended next action in this repo

Create an implementation scaffold with files like:

- `src/config.ts`
- `src/models.ts`
- `src/status.ts`
- `src/errors.ts`
- `src/provider.ts`
- `src/tools/generateImage.ts`
- `src/tools/generateVideo.ts`
- `src/tools/getRequestStatus.ts`
- `src/tools/cancelRequest.ts`
- `src/tools/listModels.ts`

That would be the moment we’ve properly started writing extension code.
