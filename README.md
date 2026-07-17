# Agent Cookbook

Portable Codex instructions and skill packages used across local projects.

## Contents

- `AGENTS.md` defines global planning, communication, Jolli, Git, and continuous-improvement behavior.
- `commit.md` defines the test, checkpoint, commit, push, and deploy workflow.
- `transport.md` documents reliable shell, SSH, API, encoding, authentication, and retry practices.
- `skills/` contains complete skill packages with their scripts, references, tests, and assets.

The repository lives directly in `~/.codex`, but its deny-all `.gitignore` permits only these portable files. Credentials, configuration, sessions, logs, databases, caches, attachments, and other machine-local runtime state must never be tracked.
