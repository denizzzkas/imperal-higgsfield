# MVP Scope

## Included in MVP

### Billing and auth
- Managed billing mode only
- Provider-managed Higgsfield Cloud credentials only
- No user-provided Higgsfield credentials

### Core capabilities
- Submit image generation requests
- Submit supported video generation requests
- Poll request status by request ID
- Cancel request by request ID
- Return result URLs

### Product controls
- Curated model allowlist
- Tiered pricing map
- Normalized statuses
- Normalized error codes

## Excluded from MVP

### Auth modes
- Bring Your Own Higgsfield API Key
- local CLI-based auth or execution
- standard Higgsfield subscriber-account login flows

### Advanced capabilities
- full catalog discovery
- webhooks
- advanced workflow builder
- user-specific billing-mode switching
- personal provider-account passthrough

## Success criteria

The MVP is successful if a user can:

1. generate an image through Imperal
2. generate a supported video request through Imperal
3. check request status reliably
4. receive clear final output or normalized failure
5. pay only with Imperal tokens

## Immediate next step after this doc

Draft `app.ir.json` for the managed-only tool surface.
