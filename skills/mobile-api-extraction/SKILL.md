---
name: mobile-api-extraction
description: Extract and verify private HTTP API behavior from user-owned Android apps and web clients. Use when Codex must inspect legitimate local sessions or client artifacts, prove requests, capture traffic, map Retrofit or similar annotations, statically inspect APKs, document endpoint evidence, diagnose authentication or challenge responses, safely verify reversible writes, or prepare a technology-agnostic implementation handoff without exposing secrets.
---

# Mobile API Extraction

Extract behavior only from clients, accounts, devices, and sessions the user owns or is authorized to test. Prefer the least invasive source that can prove the claim.

## Start safely

1. Confirm target ownership, requested behavior, allowed artifacts, and whether any write is authorized.
2. Inventory tools and artifacts without printing secret values. Record file types, paths, timestamps, app versions, session key names, and redaction needs.
3. Create an ignored/private working directory outside version control. Never commit or share credentials, sessions, cookies, tokens, HARs, APKs, decompiled output, personal/payment data, or full raw responses.
4. Define the smallest evidence question: one endpoint, one state transition, or one missing field.

Read [references/capture-and-static-analysis.md](references/capture-and-static-analysis.md) when traffic capture, Android tooling, APK/JADX, obfuscation, or client-model extraction is needed. Read [references/evidence-report-template.md](references/evidence-report-template.md) before reporting any endpoint. Read [references/implementation-handoff.md](references/implementation-handoff.md) only when implementation is requested.

## Follow the discovery ladder

Advance only when the current rung cannot supply sufficient evidence:

1. **Official/public material** — inspect documentation, help pages, published schemas, standards, and normal browser behavior. Label private endpoints as unstable.
2. **Existing app or web artifacts** — inspect source, bundles, DevTools metadata, local session structure, configuration, logs, and previously captured request summaries. Do not reveal values.
3. **Minimal raw request** — reproduce one read with the user's authenticated session. Log only method, redacted URL/path, status, content type, byte count, timing, and schema keys/types.
4. **Proxy capture** — use a test browser/device/emulator plus an intercepting proxy when ordinary trust configuration works. Trigger one action and retain only a sanitized evidence summary.
5. **Static APK analysis** — use APK/JADX inspection when capture is incomplete, pinned, noisy, or blocked. Map HTTP annotations, interfaces, models, serializers, base URLs, interceptors, and call sites.
6. **Optional implementation handoff** — proceed only after the raw call is proved; keep it technology-agnostic unless the user names a target.

Stop at the earliest rung that proves the claim. Treat capture and static analysis as complementary evidence, not automatic permission for deeper instrumentation.

## Prove each endpoint

Create one evidence-ledger row per endpoint. Do not call an endpoint “verified” unless evidence covers:

- HTTP method and normalized path;
- authentication scheme and required header **names**;
- request body/query/path schema, including required and optional fields;
- identifier source and semantics, especially display/global IDs versus user-specific/write IDs;
- observed and expected success/error status codes;
- redacted response-shape summary with keys, container types, nullability, and state fields;
- evidence source and confidence: observed live, captured, statically derived, inferred, or unverified.

Separate facts from inference. Resolve disagreements with the smallest safe raw request. Fail closed on unexplained `401`, `403`, `428`, redirects, HTML challenges, empty required bodies, or unknown schemas.

## Handle authentication and challenges

Treat `401`, `403`, and challenge responses as diagnostic puzzles: compare legitimate browser/app state, request ordering, cookies or token freshness, CSRF/nonces, client headers, redirects, clocks, and documented challenge flows. Reproduce only the normal authorized client flow.

Never bypass login, authorization, CAPTCHA, account controls, rate limits, or access boundaries. Let the user complete interactive login/CAPTCHA steps. Automation may drive an ordinary browser/client flow when authorized, but must not defeat the control. Do not brute-force, forge identity, or broaden access.

## Verify writes reversibly

Never mutate without explicit authorization or a clearly reversible local test case using an already authenticated test session. Prefer a non-sensitive object and perform the full sequence in one controlled run:

1. Read and record the initial state as a redacted summary.
2. Perform exactly one write.
3. Read again and verify the intended transition.
4. Perform the inverse write.
5. Read again and verify exact restoration.

Stop on any failed step. Attempt restoration when safe, report residual state immediately, and never hide cleanup failure. Do not test irreversible operations, purchases, payments, deletion without recovery, consent changes, or effects on other people.

## Gate deep analysis

Do not use certificate-unpinning, Frida, binary patching, repackaging, runtime hooks, custom trust bypasses, or similar techniques unless the user separately and explicitly authorizes that technique for the target. Before use, state the exact technique, risk, artifact impact, and cleanup plan. Prefer static analysis first.

## Finish

Deliver a redacted evidence report, blockers and uncertainty, artifact handling/cleanup notes, tool versions, and—only when requested—the checklist in [references/implementation-handoff.md](references/implementation-handoff.md). Never include reusable secret material or raw private payloads.
