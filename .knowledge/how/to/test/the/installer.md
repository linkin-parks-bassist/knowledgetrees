---
verified_at: '2026-09-12T14:54:05+10:00'
verified_by: codex /root
scope: knowledgetrees repository
source: tests/test-install.py and tools/verify-knowledgetree-proofs
verification: Ran the isolated-home installer integration test and both repository proof sweeps; added regression checks for session-boundary bootstrap wording.
review_when: Recheck when installer behavior, target paths, or test coverage changes.
---

Run `python3 -B tests/test-install.py`. The test uses temporary target homes and
checks dry-run behavior, knowledge installation, spine exclusion, empty-orientation
creation and preservation, existing `AGENTS.md` and Codex configuration preservation,
idempotency, conflict refusal, forced replacement, verifier execution, and same-device
same-inode hard links for both compatibility skill entry points. It also rejects a
regression to per-task skill invocation in the installed procedure or `AGENTS.md`.
