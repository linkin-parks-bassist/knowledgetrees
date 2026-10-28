---
status: green
revised_at: "2026-10-28T22:52:52+11:00"
---

Run `python3 tests/benchmark-kt.py --baseline /path/to/old-kt --repeats 5` from the checkout. Save the old CLI before editing; the baseline must be a standalone compatible `kt` script. Omit `--baseline` for current timings only. `--leaves` and `--roots` control corpus size and registered-root count.

The benchmark creates temporary knowledge trees, HOME, policy configuration, and state. It removes inherited KT/session identity variables, so it neither searches personal trees nor prunes real approvals. It measures complete subprocess wall time for a widening miss, ranked search, grep, dictionary, status, and an exact read. Each version is warmed once; measured calls are interleaved, and the reported value is the median. It compares stdout, stderr, and exit status for every run and fails if they differ. There is no timing pass threshold, and the script is outside the `test-*.py` regression glob.

Use `python3 -m cProfile -s cumulative tools/kt ...` separately to locate hot functions. Profiling overhead is substantial; compare wall times for user-visible improvement. Warm synthetic results do not establish cold disk performance or a universal speedup. A real-tree miss token must be absent from the corpus, including benchmark documentation, or the query can become a hit and change widening behavior.
