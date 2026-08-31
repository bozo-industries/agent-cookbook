# Global Agent Instructions

## Cookbook Location

Install this cookbook directly at `~/.codex` and keep its global instructions, workflow references, and skills there only. Do not copy, symlink, or track cookbook files such as `AGENTS.md`, `commit.md`, or `transport.md` inside project repositories. Relative links in this file intentionally resolve within the user-level `.codex` checkout; project-specific guidance belongs in project-owned contribution or documentation files.

## Document Freshness

At the start of every task, before implementation or any mutation, identify the local Markdown instructions and reference documents that may guide the work. Before relying on each document, perform a targeted read-only freshness check against that exact file on its known GitHub upstream and branch. For this cookbook, the canonical upstream is `bozo-industries/agent-cookbook` on `master`. For project documents, use an explicitly known source mapping or derive the repository, branch, and relative path from the local Git metadata when available.

Never assume the local directory is a Git clone. Do not run a broad pull, fetch, checkout, reset, repository scan, or bulk synchronization for this check. Query only the individual GitHub file through the API or raw-file endpoint and compare its hash or content with the local copy. Prefer authenticated GitHub API or CLI requests when credentials are available, and retry that way when an unauthenticated raw-file request returns `404` for a private or auth-required repository; do not treat that `404` alone as proof the document is missing. If GitHub has a different version, read it before acting, report the discrepancy when material, and follow the newest applicable guidance without silently overwriting local changes. If a document has no known GitHub source or the targeted check is unavailable, say so briefly when relevant and continue from the local copy; never upload local contents merely to perform a freshness check.

## Communication Verbosity

Use an oververbosity target of 4/10 by default, expressed as `40% volume` through the user-facing alias.

Treat `volume` as a percentage-only user-facing alias for `oververbosity`. Map the scales linearly: every 10 percentage points of volume equals one oververbosity point, so `60% volume` means 6/10 oververbosity. Always write volume with `%`; never use `/10` notation for volume.

- Use 0/10 oververbosity when the user requests `0% volume`. Treat this as execution-only mode: spend tokens on inspecting, changing, testing, committing, pushing, deploying, or otherwise directly advancing the requested result—not on narrating the work. Do not restate the request, announce plans, explain routine choices, provide conversational progress, or produce optional summaries. Keep reasoning internal. Send user-visible text only when required by the platform or necessary for a blocker, safety issue, permission or deployment decision, material failure, or minimal verifiable completion record; make that text as terse as possible. Zero volume never permits skipping validation, concealing uncertainty or failures, bypassing required approval, or weakening safety.
- Use 1/10 when the user explicitly asks for a task to be done `autonomously`. Keep progress updates and the final handoff minimal while still reporting blockers, material risks, verification, commits, pushes, and deployment status.
- Use 7/10 when the user is present and evidently steering or managing the work through active feedback, follow-up instructions, or iterative decisions. Provide enough detail for close collaboration and easy course correction.
- Return to 4/10 when neither condition applies. A direct user request for a different response length or level of detail overrides these defaults.

## Planning

Start substantial work in Plan mode before implementation. This includes new features, refactors, migrations, architectural changes, cross-cutting work, and any task with multiple meaningful steps, unclear scope, or important tradeoffs. Use the planning phase to inspect the relevant system, identify risks and dependencies, define verification, and resolve decisions that could materially change the implementation.

Plan mode may be skipped only for genuinely small, obvious, low-risk changes that are faster to implement than to formally plan, and for narrow time-sensitive bug fixes where delay matters. When Plan mode is unavailable, write and maintain an explicit implementation plan before changing code.

## Discord Input Notifications

During the first Plan mode phase of each task that enters Plan mode, ask once whether the user wants Discord notifications when their input is required. Use the planning-mode blocking question feature by calling `request_user_input` without `autoResolutionMs`. Make clear that the webhook is optional, recommend continuing without one, and tell the user to paste a Discord webhook URL in the question's free-form `Other` field if they want notifications. If the user declines, submits no URL, or supplies an invalid URL, continue without Discord notifications. Once supplied, the webhook remains active for the entire task, not only during planning.

Treat a supplied webhook URL as a task-scoped secret: keep it only for the current task; never echo, log, persist, commit, or expose it in command arguments or output; and do not send a test message. The notification requirement applies throughout planning, implementation, testing, verification, commit, push, deployment, and operational work. Immediately before asking, instructing, or waiting for any user response or user-performed action required to continue, use the webhook once to send only `<@939406522742611979> Codex needs your input in the current task. Please return to Codex.`, with allowed mentions restricted to Discord user ID `939406522742611979`. This includes clarifications, decisions, approvals, authentication or permission steps, sign-ins, MFA or captcha, actions in a browser, device, emulator, or provider UI, supplying a needed file or secret through an appropriate secure channel, and resolving any other execution blocker. The trigger is needing the user, regardless of the current collaboration mode or whether `request_user_input` is available: in Plan mode, notify immediately before the blocking question; outside Plan mode, notify immediately before yielding with the request or otherwise pausing for the user.

Do not include task details, user data, secrets, or the request itself in the Discord message, and do not notify for non-blocking questions, routine updates, or completion messages that require no user action. A failed notification must not delay the in-app request; report only a sanitized delivery failure and continue waiting in Codex.

## Jolli Memory

Jolli is the durable development memory built from the repository's commits. Use its repository-provided skills whenever historical context can materially improve the work:

- Use `jolli-recall` when resuming a branch or when its prior plans, decisions, and development context are needed.
- Use `jolli-search` when looking across branches for earlier decisions, related commits, files, tickets, or prior solutions to a topic. Search before making a substantial design decision when the repository is likely to contain relevant precedent.
- Use `jolli-pr` whenever creating or updating a pull request so its title and description are grounded in the recorded commit memory. Follow that skill's queue, push, and PR-update workflow exactly.

Jolli complements current repository inspection; it does not replace reading the relevant code, diffs, tests, and documentation. Do not invoke it mechanically for trivial work with no relevant history. If a needed Jolli capability is unavailable or has no record, report that plainly and continue with direct repository evidence when possible.

## Git Workflow

For any task that changes a Git worktree, read and follow [commit.md](./commit.md) from the user-level `.codex` checkout. Project-owned contribution guides may add stricter requirements without copying the cookbook into that repository.

## Shell, SSH, and APIs

For work involving shell boundaries, SSH, HTTP APIs, JSON payloads, encodings, or network retries, read and follow [transport.md](./transport.md) from the user-level `.codex` checkout.

## Android Instrumentation Packaging

Before installing or running Android instrumentation after main-source changes, build both the
target application APK and the test APK in the same Gradle invocation (for example,
`assembleDebug assembleDebugAndroidTest`). Building only `assembleDebugAndroidTest` can leave a
stale target APK beside a newly compiled test APK and produce misleading `NoSuchMethodError`
failures on-device.

## KiCad Automation

For work using KiCad's Python bindings or command-line validation, read and follow [kicad.md](./kicad.md) from the user-level `.codex` checkout.

## Blender Automation

For work using Blender's Python API or background rendering, read and follow [blender.md](./blender.md) from the user-level `.codex` checkout.

## Continuous Instruction Improvement

When an execution error reveals a reusable pitfall in the environment, tooling, shell syntax, encoding, authentication, API behavior, Git workflow, or deployment process, fix the immediate problem and update the relevant agent instruction document during the same task. Record the preventive rule and correct technique, not a chronological incident report. Keep one-off outages, obvious typos, transient provider failures, secrets, credentials, and private payloads out of the instructions. If no existing document fits, create a small focused Markdown guide and reference it from this file. Validate, commit, and push instruction improvements as their own coherent checkpoint.
