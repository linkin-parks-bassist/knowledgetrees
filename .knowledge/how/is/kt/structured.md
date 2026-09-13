---
status: "unverified"
created_at: "2026-09-13T13:46:44+10:00"
scope: "local"
source: "tools/kt implementation review and current regression suites"
---

The CLI remains one self-contained standard-library Python executable for standalone installation. Sections separate root discovery and access, lookup and rendering, leaf maintenance, capture, proof execution, and parser construction. RootAccessView loads discovery and policies once per invocation; LookupContext lazily reads permitted leaf text once. LeafSnapshot centralizes revision and inode checks for amendment and destructive maintenance. command_parser separates command schemas and handler dispatch from execution. The standalone verifier delegates to the embedded proof engine. Regression suites cover access, lookup, maintenance, installation, hooks, and proof timestamps.
