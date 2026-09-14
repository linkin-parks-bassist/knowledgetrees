---
status: "unverified"
created_at: "2026-09-13T13:46:44+10:00"
scope: "local"
source: "tools/kt built-in proof engine; installer; owner removal of separate verifier"
updated_at: "2026-09-13T13:54:30+10:00"
---

The CLI remains one self-contained standard-library Python executable for standalone installation. Sections separate root discovery and access, lookup and rendering, leaf maintenance, capture, proof execution, and parser construction. RootAccessView loads discovery and policies once per invocation; LookupContext lazily reads permitted leaf text once. LeafSnapshot centralizes revision and inode checks for amendment and destructive maintenance. command_parser separates command schemas and handler dispatch from execution. All verification is exposed through kt prove. Regression suites cover access, lookup, maintenance, installation, hooks, and proof timestamps.

`kt rewrite ADDRESS CONTENTS` shares the amend handler, supplying literal inline
Markdown instead of file/stdin input. Its optional --expect checks prior context;
without it the locked current snapshot supplies the base. Final snapshot checks,
hardlinks, access policy, review invalidation and proof handling remain shared.
Evidence: tools/kt and tests/test-amend.py, 2026-09-15.

Successful rewrite returns the locked original text, explicitly superseded, and a
semantic-loss review reminder; it does not echo the new text. No-ops label returned
contents unchanged; dry-run remains a diff. Evidence: source/tests, 2026-09-15.
