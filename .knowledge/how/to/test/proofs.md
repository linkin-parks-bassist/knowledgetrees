---
status: green
revised_at: "2026-10-01T07:50:31+10:00"
---

Run `python3 -B tests/test-proofs.py`. It checks that every executable predicate
uses the exact, timeless `Proof:` delimiter; proof evaluation never stores a
per-proof outcome or timestamp. It accepts both `_` and concrete legacy validation
stamps, leaves them untouched under `--no-stamp`, and silently migrates them to
`Proof:` on a writing run. It covers lifecycle status
transitions, unchanged manual `checked_at`, sticky brown behavior, independent
clearance, fully read-only `--no-stamp`, proof-free leaves, malformed decorated
markers, flat skill metadata, preserved hardlink identity, and the absence of
steady-state file churn.

Recurring-expiry fixtures derive their timestamps from the current UTC time:
the green fixture is checked now and the expired fixture three weeks earlier.
Their two-week intervals therefore exercise both states without a fixed calendar
deadline making the test stale.

The test also covers the `verifiable: true` exception: complete passing proofs
clear sticky falsification and write green while leaving the answer bytes
unchanged; a zero-proof declaration, invalid Boolean value, skipped proof, or
failing proof becomes brown.

Run `python3 -B tests/test-metadata.py` for the flat schema, manual
whole-leaf `checked_at` timestamp, rejected unsupported fields and date-only
timestamps, and `verifiable: true` preservation through rewrite.
