---
verified_at: '2026-09-12T12:06:21+00:00'
verified_by: codex /root
scope: knowledgetrees repository
source: tests/test-install.py and tools/verify-knowledgetree-proofs
verification: Ran installer, shared-hook, and mock OpenCode adapter checks; reviewed successful proof-stamp normalization and protected falsification/content differences.
review_when: Recheck when installer behavior, target paths, or test coverage changes.
---

Run `python3 -B tests/test-install.py`. The test uses temporary target homes and
checks dry-run behavior, knowledge installation, spine exclusion, empty-orientation
creation and preservation, existing `AGENTS.md` and Codex configuration preservation,
idempotency, conflict refusal, forced replacement, verifier execution, and same-device
same-inode hard links for both compatibility skill entry points. It also rejects a
regression to per-task skill invocation in the installed procedure or `AGENTS.md`.

Hook integration also checks safe Codex merge, malformed-hook refusal before writes,
dedicated Copilot event definitions, OpenCode adapter deployment, idempotent hook
installation, and `--hooks-only` preservation of customized leaves, hardlinks, and
permissions. Run `python3 -B tests/test-hooks.py` for shared protocol tests and
`node tests/test-opencode-hooks.mjs` for the mocked OpenCode adapter. Neither runs
models. Run `python3 -B tests/test-kt.py` for retrieval and weak-result exit checks.

Successful proof timestamp refreshes alone are not installation content conflicts;
their installed stamps are retained until the verifier checks them again. Falsified
markers, sticky leaf falsification flags, prose edits, and other metadata changes
remain protected content differences. Reinstallation tests cover both cases.
