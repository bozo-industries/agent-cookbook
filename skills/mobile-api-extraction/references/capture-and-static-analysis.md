# Capture and static analysis

## Contents

- Artifact and session inspection
- Minimal raw proof
- Browser and web-client inspection
- Android emulator and proxy capture
- Static APK/JADX workflow
- Retrofit and model mapping
- Authentication diagnostics
- Tooling baseline

## Artifact and session inspection

Inventory filenames, formats, timestamps, app versions, package names, hosts, and JSON key names without printing values. Check ignored/private storage before reading. Prefer metadata commands and small parsers that emit booleans, counts, types, sizes, or hashes.

For web clients, inspect source maps, minified bundles, service workers, network initiators, storage **key names**, cookie attributes, request constructors, GraphQL documents, and normal browser requests. Do not export a whole browser profile.

For Android clients, inventory the APK/split set, package/version, manifest, network-security config, native libraries, DEX files, and any existing decompiled tree. Never place APKs or output in the skill or repository.

## Minimal raw proof

Build a disposable local probe with secrets loaded at runtime. Never embed them in code or command arguments. Emit only:

```text
method, normalized path, status, content-type, byte count, duration
top-level type, redacted key/type summary, pagination/state field names
```

Start with one read. Preserve request ordering, token refresh rules, CSRF/nonces, cookies, and context headers only when evidence says they are required. Avoid retry storms. If refresh tokens rotate, persist the new token atomically only after a parsed successful response; otherwise use the established client/session manager.

## Browser and web-client inspection

Use DevTools or browser automation to trigger one normal action. Correlate the user action with its initiator and request. A small copy-as-fetch/cURL can seed a sanitized raw probe, but remove all secret values before saving notes. Treat browser challenges as part of the legitimate flow, not a target to evade.

## Android emulator and proxy capture

1. Use a user-owned APK and test account/session.
2. Start a disposable emulator/AVD; record API level and root/Play Services constraints.
3. Start the intercepting proxy and configure the emulator host address (commonly `10.0.2.2:<port>` on the standard Android emulator).
4. Install the proxy CA through supported device trust configuration. Use a writable/rootable test image only for ordinary CA placement.
5. Smoke-test DNS, TCP reachability, proxy routing, and a browser HTTPS request.
6. Install/launch the app, authenticate normally, and trigger one target action.
7. Extract a sanitized request/response-shape summary, then clear the proxy and stop the emulator.

If traffic is CONNECT-only, TLS fails, the app rejects the trust store, Play Integrity blocks the emulator, or the action produces no relevant traffic, record the blocker and move to static analysis. Do not silently add unpinning or patching.

## Static APK/JADX workflow

Decompile privately:

```powershell
jadx -d <private-output-dir> <user-owned.apk>
```

Search narrowly with `rg`:

```powershell
rg -n "endpoint-fragment|oauth|token|activation|delete|update" <jadx>/sources
rg -n "@GET|@POST|@PUT|@PATCH|@DELETE|@Headers|@Header|@Body|@Path|@Query" <jadx>/sources
rg -n "SerializedName|Json\(|JsonProperty|JsonAdapter|Serializer|Deserializer" <jadx>/sources
```

For obfuscated apps, locate the service interface first, then map annotation definitions by tracing where the HTTP framework parses them. Do not assume an obfuscated annotation means a verb solely from its shape. Cross-check framework parser branches, known interfaces, or call behavior.

Trace:

1. Base URL construction and environment selection.
2. Service/interface method annotations and return wrapper.
3. Path, query, header, field, multipart, and body annotations.
4. Request model plus generated/custom serializer.
5. Response model plus generated/custom adapter.
6. Interceptors that add authentication, locale, device/app version, signature, CSRF, or correlation headers.
7. Call sites that supply identifiers and default values.
8. UI/domain mapping that reveals state transitions and identifier meaning.

## Retrofit and model mapping

Create a local mapping table for annotations:

| Obfuscated annotation | Meaning | Proof source |
| --- | --- | --- |
| `@x(...)` | GET/POST/etc. | Retrofit parser branch or known declaration |
| `@y("name")` | Header/Path/Query | Parameter parser and emitted request |
| `@z` | Body | Converter invocation and serializer |

Open every referenced request/response class. Record serialized JSON names, types, nullable/default behavior, nested collections, discriminators, and error envelopes. Use call sites to decide whether an ID comes from `list[].id`, a global catalog field, URL, account context, or generated client value.

Do not claim success statuses from annotations alone. Static declarations prove intent; sanitized raw requests prove runtime behavior.

## Authentication diagnostics

For `401`, `403`, `428`, challenge HTML, or redirects, compare:

- token audience/scope/expiry and refresh rotation;
- cookies, SameSite/domain/path attributes, CSRF pairings, and nonce ordering;
- locale/country/tenant/store/device/app-version context;
- origin/referer and browser fetch mode where genuinely required;
- clock skew, redirect chain, and content negotiation;
- whether the endpoint expects a user-specific identifier;
- rate-limit or bot/challenge responses.

Repeat the normal authorized flow or ask the user to complete interactive login/CAPTCHA. Never defeat the control.

## Tooling baseline

Install only what the chosen rung requires and report versions:

- Android SDK Platform Tools (`adb`) and Emulator for Android capture;
- a disposable AVD/system image appropriate for the owned app;
- an intercepting proxy such as HTTP Toolkit, mitmproxy, or Burp configured for local testing;
- Java and JADX for static APK inspection;
- `rg` plus a local scripting runtime for sanitized probes;
- browser DevTools/automation for web clients.

Add stable executable directories to the user PATH without replacing existing entries. Verify commands in a fresh shell. Frida, unpinning modules, repackaging, and patching tools are not baseline dependencies; install/use them only after separate explicit authorization.
