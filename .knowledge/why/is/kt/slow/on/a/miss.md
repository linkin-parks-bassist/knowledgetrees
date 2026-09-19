---
status: green
revised_at: "2026-09-13T13:51:54+10:00"
---

A miss widens through semantic ancestors and scans eligible leaves. In this checkout, the same deliberately absent query improved from about 3.02 seconds to 0.58 seconds under cProfile after replacing repeated root discovery and policy loading with an invocation-local RootAccessView and lazy LookupContext. A normal unprofiled run was about 0.18 seconds. These are measurements for this machine and corpus, not general latency guarantees. No persistent cache or model is required; every invocation reloads current policies and content. A future native rewrite is an owner-suggested possibility, not an agreed implementation: measure warm/cold filesystem runs and separate interpreter startup, traversal, parsing, and ranking before selecting it.

The existing profile does not establish a disk-I/O/allocation time split. CPython pymalloc pools small objects of up to 512 bytes in arenas, so object allocation does not imply an OS allocation syscall per object (Python 3.12 C API memory documentation: https://docs.python.org/3.12/c-api/memory.html). A native design with query-lifetime arenas and compact records could reduce allocation and object overhead; its benefit for kt remains unmeasured.
