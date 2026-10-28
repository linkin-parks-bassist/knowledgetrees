---
status: green
revised_at: "2026-10-28T22:53:30+11:00"
---

A miss widens through semantic ancestors and scans eligible leaves. On Python 3.12, `Path.is_relative_to` constructs ancestor objects; calling it for every visited path against every registered root dominated retrieval. `RootAccessView` now precomputes root-component tuples deepest first. Each candidate is still resolved canonically before matching, preserving symlink resolution and nested-root boundaries. Configured policy paths are canonicalized once per access view instead of once per root. `roots()` uses that same view rather than repeatedly loading configuration. No persistent content or permission cache is used.

An isolated warm benchmark with 512 leaves and 26 roots, using three interleaved measured runs per version, produced these median subprocess wall times before and after optimization:

| Operation | Before | After | Speedup |
| --- | ---: | ---: | ---: |
| Widening miss | 1,959.77 ms | 211.96 ms | 9.25× |
| Ranked search | 789.90 ms | 114.01 ms | 6.93× |
| Grep | 773.46 ms | 110.30 ms | 7.01× |
| Status | 770.91 ms | 99.23 ms | 7.77× |
| Dictionary | 88.66 ms | 77.40 ms | 1.15× |
| Exact read | 64.41 ms | 52.96 ms | 1.22× |

All compared stdout, stderr, and exit statuses matched. These are machine/corpus-specific measurements, not latency guarantees or cold-disk results. Run `tests/benchmark-kt.py`; the procedure is `how/to/benchmark/kt.md`. A profile on a larger accessible corpus identified the ownership bottleneck, reducing an otherwise unchanged miss from 39.510 to 1.173 profiled seconds with the component-prefix change alone. Profile timings include substantial instrumentation overhead.

Further work should measure canonical path resolution, traversal, and interpreter startup before selecting a native rewrite or persistent cache. Neither is required by the current design.
