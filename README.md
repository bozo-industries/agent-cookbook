# Agent Cookbook

Portable Codex instructions and skill packages used across local projects.

## Contents

- `AGENTS.md` defines global planning, communication, Jolli, Git, and continuous-improvement behavior.
- `commit.md` defines the test, checkpoint, commit, push, and deploy workflow.
- `transport.md` documents reliable shell, SSH, API, encoding, authentication, and retry practices.
- `skills/` contains complete skill packages with their scripts, references, tests, and assets.
- `skills/apk-reverse/` provides a workflow for analyzing Android APKs and verifying client-side changes on authorized targets; its MIT license is included with the skill.
- `skills/icon-generation/` creates individual icons and coherent multi-group collections with reference-grounded style continuity.
- `skills/playwright/` provides browser automation workflows using Microsoft's Playwright CLI, adapted for Codex.

The repository lives directly in `~/.codex`, but its deny-all `.gitignore` permits only these portable files. Credentials, configuration, sessions, logs, databases, caches, attachments, and other machine-local runtime state must never be tracked.

Keep this cookbook user-level: do not copy, symlink, or commit its instruction files or skills inside individual project repositories. Projects may keep their own contribution and architecture documentation, while global cookbook references continue to resolve from `~/.codex`.
