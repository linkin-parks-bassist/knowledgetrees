---
scope: knowledgetrees repository
source: "tools/kt built-in proof engine; installer; owner removal of separate verifier"
review_when: Recheck after changes to marker parsing, outcome stamping, or leaf falsification.
status: "unverified"
updated_at: "2026-09-13T13:54:30+10:00"
---

Run `python3 -B tests/test-proof-stamps.py`. It checks legacy-marker migration,
per-proof success and failure timestamps, unchanged leaf `verified_at`, sticky
leaf falsification even after proofs recover, explicit independent clearance,
read-only mode, proof-free leaves, malformed markers, nested skill metadata, and
preserved hardlink identity.
