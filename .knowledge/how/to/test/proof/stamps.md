---
scope: knowledgetrees repository
source: "tests/test-proof-stamps.py engine selector; both entry points passed"
review_when: Recheck after changes to marker parsing, outcome stamping, or leaf falsification.
status: "unverified"
updated_at: "2026-09-13T13:52:11+10:00"
---

Run `python3 -B tests/test-proof-stamps.py`. It checks legacy-marker migration,
per-proof success and failure timestamps, unchanged leaf `verified_at`, sticky
leaf falsification even after proofs recover, explicit independent clearance,
read-only mode, proof-free leaves, malformed markers, nested skill metadata, and
preserved hardlink identity.

Also run `KT_TEST_BUILTIN_PROOFS=1 python3 -B tests/test-proof-stamps.py`
to exercise the same contract through kt prove instead of its compatibility entry point.
