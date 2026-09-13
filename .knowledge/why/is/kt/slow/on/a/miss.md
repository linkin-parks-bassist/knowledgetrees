---
status: "unverified"
updated_at: "2026-09-13T13:46:57+10:00"
source: "Before/after cProfile and unprofiled measurements in this checkout; tools/kt RootAccessView/LookupContext; owner native-rewrite suggestion"
---

A miss widens through semantic ancestors and scans eligible leaves. In this checkout, the same deliberately absent query improved from about 3.02 seconds to 0.58 seconds under cProfile after replacing repeated root discovery and policy loading with an invocation-local RootAccessView and lazy LookupContext. A normal unprofiled run was about 0.18 seconds. These are measurements for this machine and corpus, not general latency guarantees. No persistent cache or model is required; every invocation reloads current policies and content. A future native rewrite is an owner-suggested possibility, not an agreed implementation: measure warm/cold filesystem runs and separate interpreter startup, traversal, parsing, and ranking before selecting it.