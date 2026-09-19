---
status: green
revised_at: "2026-09-20T08:51:45+10:00"
---

Run `python3 -B tests/test-proof-stamps.py`. It checks expiry-driven passing timestamps,
non-expiring marker stability, failure transitions, unchanged manual `checked_at`, sticky
leaf falsification even after proofs recover, explicit independent clearance,
read-only mode, proof-free leaves, malformed markers, nested skill metadata, and
preserved hardlink identity. It also checks the `verifiable: true` exception:
complete passing proofs clear sticky falsification without creating a leaf-level proof time,
and write green while retaining non-expiring proof markers, while a zero-proof declaration or
invalid Boolean value becomes brown.

Run `python3 -B tests/test-metadata.py` for the legacy date-only `checked_at`
compatibility case. Such a date must not cause sticky falsification, especially
when the leaf has no executable proofs. Malformed freshness values warn yellow.
