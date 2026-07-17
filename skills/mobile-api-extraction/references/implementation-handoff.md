# Technology-agnostic implementation handoff

Use only after at least one minimal raw request succeeds. Do not prescribe a framework, repository, service layout, or daemon.

## Contract

- [ ] Record base URL/environment selection separately from normalized endpoint paths.
- [ ] Define method, path/query/body schema, required header names, identifier semantics, success codes, and redacted error shapes.
- [ ] Label private endpoints unstable and note the observed client/version/date.
- [ ] Represent authentication as injected session material; never embed credentials.
- [ ] Specify refresh/rotation and atomic persistence behavior where applicable.

## Behavior

- [ ] Preserve request ordering, context headers, pagination, nullability, and content negotiation proved by evidence.
- [ ] Normalize the write-compatible identifier, not merely a display/catalog ID.
- [ ] Fail closed on authentication/challenge/schema errors.
- [ ] Bound response sizes, timeouts, pagination, retries, and rate.
- [ ] Keep browser/emulator/proxy discovery outside routine execution unless explicitly required.

## Tests

- [ ] Assert URL, verb, required header names, query/body serialization, and identifier source.
- [ ] Cover representative redacted response and error shapes.
- [ ] Cover token refresh/rotation without logging values.
- [ ] Cover filtering, pagination, state normalization, and unknown-schema failure.
- [ ] For writes, test read → write → verify → inverse → restoration using mocks or an explicitly authorized test session.

## Operations and privacy

- [ ] Load secrets from an approved private store and redact logs/errors.
- [ ] Exclude sessions, captures, APKs, decompiled output, and raw responses from version control and packaging.
- [ ] Document recapture/revalidation triggers: client release, schema drift, auth errors, or endpoint retirement.
- [ ] Provide a disable/rollback path and avoid irreversible background writes.
- [ ] Review the final diff/artifact set for credentials and personal/payment data.

## Handoff packet

- [ ] Redacted endpoint evidence ledger.
- [ ] Sanitized synthetic fixtures, not copied user payloads.
- [ ] Known blockers/inferences and confidence levels.
- [ ] Tool/client versions and validation date.
- [ ] Artifact cleanup/retention statement.
