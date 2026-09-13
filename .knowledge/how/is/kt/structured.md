---
status: "unverified"
created_at: "2026-09-13T13:46:44+10:00"
scope: "local"
source: "tools/kt built-in proof engine; installer; owner removal of separate verifier"
updated_at: "2026-09-13T13:54:30+10:00"
---

The CLI remains one self-contained standard-library Python executable for standalone installation. Sections separate root discovery and access, lookup and rendering, leaf maintenance, capture, proof execution, and parser construction. RootAccessView loads discovery and policies once per invocation; LookupContext lazily reads permitted leaf text once. LeafSnapshot centralizes revision and inode checks for amendment and destructive maintenance. command_parser separates command schemas and handler dispatch from execution. All verification is exposed through kt prove. Regression suites cover access, lookup, maintenance, installation, hooks, and proof timestamps.
