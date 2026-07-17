# Commit, Push, and Deploy Workflow

For every task that changes a Git worktree:

1. Work in small, coherent checkpoints. Each commit should have one reviewable purpose; do not bundle several independent features, fixes, refactors, or documentation changes into one bulk commit.
2. At each checkpoint, run the tests and checks appropriate to that change. Commit only after they pass, or clearly report any known failure or blocker.
3. Review the staged diff. Include only work in scope, and never commit unrelated user changes, generated noise, captures, credentials, or secrets.
4. Follow the repository's commit-message rules. When no stricter local rule exists, begin the imperative subject with `[feat]`, `[fix]`, `[perf]`, `[refactor]`, `[docs]`, `[test]`, `[build]`, `[ci]`, `[chore]`, or `[revert]`.
5. When repository policy permits intentionally skipping CI, put `[skip ci]` immediately after the normal tag, for example: `[docs][skip ci] Clarify deployment steps`. Never append it at the end.
   - Repository exception: never use `[skip ci]` in `bozo-industries/agent-cookbook`; use only the normal commit-type tag.
6. Push every completed, tested checkpoint to its configured remote. Do not leave finished work only in the local worktree unless pushing is technically blocked or a higher-priority instruction forbids it; report the exact blocker.
7. Deploy only after the tested commit has been pushed. If deployment is requested or is an established required step, deploy and verify it. If deployment intent is uncertain, ask before deploying. That uncertainty does not block committing and pushing.
8. Report the commit hash, pushed branch and remote, tests run, and deployment status. Never claim deployment based only on a local test or successful push.
