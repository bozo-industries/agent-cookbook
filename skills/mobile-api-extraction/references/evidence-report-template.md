# Evidence report template

Use this structure for every extraction. Omit secret values and full payloads.

## Scope and authorization

- Target/client version:
- User-owned artifacts inspected:
- Authorized reads/writes:
- Explicit deep-analysis authorization (normally none):
- Private working location and cleanup status:

## Discovery ladder

| Rung | Attempt | Evidence gained | Limitation / next decision |
| --- | --- | --- | --- |
| Official/public |  |  |  |
| Existing artifacts |  |  |  |
| Minimal raw request |  |  |  |
| Proxy capture |  |  |  |
| Static analysis |  |  |  |

## Endpoint evidence ledger

Use one row per method/path pair. “Header names” must never include values.

| Claim | Required evidence |
| --- | --- |
| Method + path | Exact verb and normalized path; redact tenant/user/object values |
| Authentication + headers | Scheme and required header names; distinguish auth, context, content negotiation, and telemetry |
| Inputs | Path/query/body fields, types, requiredness, allowed values, and a synthetic example |
| Identifier semantics | Field that supplies each identifier; scope, stability, and whether it is display/global/user-specific/write-compatible |
| Status codes | Observed success and error codes; statically suggested codes remain “expected/unverified” |
| Response shape | Top-level type and redacted keys/types; pagination, nullability, error envelope, state fields; never full data |
| Evidence + confidence | Artifact path/class, sanitized capture/probe timestamp, observation type, and confidence |

Recommended endpoint row:

```text
METHOD /normalized/path/{objectId}
Auth/header names: Bearer; Authorization, Accept, Content-Type, <context headers>
Inputs: objectId:string from list[].id; body { enabled:boolean }
Identifier: user-scoped list row ID; displayId is not accepted for writes
Statuses: 200 observed; 400/401/403 expected or observed as labeled
Response: object { id:string, enabled:boolean, ... }; values redacted
Evidence: interface annotation + serializer + sanitized raw proof; confidence high
```

## Reversible-write ledger

```text
Initial read: state=<redacted enum/bool>; status=<code>
Write: METHOD path; body shape=<schema only>; status=<code>
Verification read: expected transition observed=<yes/no>
Inverse write: METHOD path; status=<code>
Restoration read: exact initial state restored=<yes/no>
Residual risk/blocker: <none or concise description>
```

## Redaction and artifact handling

- Report only key names, types, sizes, hashes when useful, and synthetic identifiers.
- Replace user/account/device/order values with semantic placeholders.
- Keep raw captures, APKs, decompiled sources, and sessions outside version control.
- Delete temporary exports after extracting the minimum evidence, unless the user asks to retain them privately.
- Search the output and staged Git diff for token, cookie, email, phone, address, payment, and raw-payload leakage.

## Confidence language

- **Observed live:** directly returned by an authorized request in this run.
- **Captured:** directly present in sanitized traffic from the authorized client.
- **Statically derived:** declared by client code/annotations/models, not yet exercised.
- **Inferred:** supported indirectly; state the reasoning.
- **Blocked/unverified:** missing required evidence; do not implement as fact.
