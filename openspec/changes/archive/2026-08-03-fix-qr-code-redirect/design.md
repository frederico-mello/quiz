## Context

See `proposal.md` for the motivation and `specs/question-link-qr-code/spec.md` for the behavioral contract. The application already centralizes environment configuration in `src/config.py`, composes the question URL in `app.py`, and delegates QR image encoding to `src/qrcode_service.py`. `APP_URL` is currently configurable, but its fallback is a local Streamlit address. Existing tests use `pytest`, and the README documents the current fallback.

## Goals / Non-Goals

**Goals:**

- Make `https://lappquiz.ict.unesp.br` the deterministic fallback for QR code links.
- Preserve the existing `APP_URL` environment override and `?q=<id>` URL composition.
- Keep current component boundaries and QR generation interface unchanged.
- Keep configuration documentation and automated tests aligned with the new fallback.

**Non-Goals:**

- Add a URL builder service, redirect service, route, or new dependency.
- Change QR image generation, question access, answer handling, or session state.
- Validate or normalize custom `APP_URL` values beyond existing behavior.
- Rewrite QR codes that were already generated with a local address.

## Decisions

### Configuration boundary

`src/config.py` remains the single resolution point for `APP_URL`. When the environment variable is present, its value remains authoritative; otherwise, configuration resolves to `https://lappquiz.ict.unesp.br`. This uses the existing configuration seam and avoids duplicating the canonical URL in the application or QR service.

### Component structure and data flow

`app.py` continues to compose the question-specific URL from `APP_URL` and `?q=<id>`, then passes the complete URL to `generate_qr_code`. `src/qrcode_service.py` remains unaware of URL configuration and continues to encode arbitrary data as a PNG buffer. No new state, persistence, or interface is introduced.

### Failure handling

An unset `APP_URL` is handled by the public fallback, so missing configuration no longer produces a local QR destination. Custom values and QR generation failures retain current behavior. Domain availability remains an operational concern rather than something handled by the QR generator; no retry or intermediate redirect is added.

### Testing approach

Extend the existing `pytest` unit-test boundary to cover resolution with `APP_URL` absent and with a custom value, plus the final `app.py` URL composition with `?q=<id>`. Retain the existing `qrcode_service` PNG test. No browser or integration test infrastructure is required because URL composition and QR rendering boundaries remain unchanged.

### Rollout and rollback

Deploy the configuration change normally. Environments that already set `APP_URL` keep their explicit destination. Existing QR images are immutable and must be regenerated if they contain `localhost`; no data migration is required. Rollback restores the prior configuration behavior, while `APP_URL` can control destinations during an environment transition.

### Documentation consistency

Update the README's configuration reference so it describes the public fallback and the local override convention. Generated OpenWiki pages remain workflow-owned and are not edited manually.

## Risks / Trade-offs

- [Local development without `APP_URL`] → QR codes point to the public application instead of the local server; developers can set a local `APP_URL` override when local scanning is required.
- [Previously generated QR codes] → Existing images continue to encode their original local address; regenerate and redistribute them after deployment.
- [Invalid custom `APP_URL`] → The QR code can encode an inaccessible destination; configuration validation is intentionally unchanged and operators remain responsible for supplying an accessible URL.
- [Documentation drift] → A stale default could cause incorrect deployment configuration; update the README in the same change and leave generated OpenWiki refresh to its workflow.
