---
verified_at: '2026-09-12T15:33:08+10:00'
verified_by: codex /root
scope: knowledgetrees repository
source: tools/verify-knowledgetree-proofs and tests/test-proof-stamps.py
verification: Ran the focused integration test against successful, failed, malformed, nested-metadata, and previously falsified leaves.
review_when: Recheck after changes to marker parsing, outcome stamping, or leaf falsification.
---

Run `python3 -B tests/test-proof-stamps.py`. It checks legacy-marker migration,
per-proof success and failure timestamps, unchanged leaf `verified_at`, sticky
leaf falsification even after proofs recover, explicit independent clearance,
read-only mode, proof-free leaves, malformed markers, nested skill metadata, and
preserved hardlink identity.
