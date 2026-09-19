---
scope: knowledgetrees repository
source: "tools/kt built-in proof engine; installer; owner removal of separate verifier"
review_when: Recheck after changes to marker parsing, outcome stamping, or leaf falsification.
status: "unverified"
updated_at: "2026-09-13T13:54:30+10:00"
---
Status: Green

Run `python3 -B tests/test-proof-stamps.py`. It checks expiry-driven passing timestamps,
non-expiring marker stability, failure transitions, unchanged leaf `verified_at`, sticky
leaf falsification even after proofs recover, explicit independent clearance,
read-only mode, proof-free leaves, malformed markers, nested skill metadata, and
preserved hardlink identity. It also checks the `verifiable: true` exception:
complete passing proofs create whole-leaf `verified_at`, clear sticky falsification,
and write green without later non-expiry churn, while a zero-proof declaration or
invalid Boolean value becomes brown.
