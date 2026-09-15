---
status: "unverified"
created_at: "2026-09-13T13:46:44+10:00"
scope: "local"
source: "tools/kt built-in proof engine; installer; owner removal of separate verifier"
updated_at: "2026-09-13T13:54:30+10:00"
---

The CLI remains one self-contained standard-library Python executable for standalone installation. Sections separate root discovery and access, lookup and rendering, leaf maintenance, capture, proof execution, and parser construction. RootAccessView loads discovery and policies once per invocation; LookupContext lazily reads permitted leaf text once. LeafSnapshot centralizes revision and inode checks for amendment and destructive maintenance. command_parser separates command schemas and handler dispatch from execution. All verification is exposed through kt prove. Regression suites cover access, lookup, maintenance, installation, hooks, and proof timestamps.

`kt rewrite ADDRESS HASH CONTENTS` shares the amend handler with a mandatory
positional SHA-256 revision and literal inline Markdown. Full open/exact-question
reads always print the hash of the same returned bytes on stderr. --revision is a
compatibility no-op. Rewrite checks the required hash against the locked snapshot
and retains final inode/content checks, hardlinks, access controls, review and
proof handling. Success and no-ops are silent (exit 0); dry-run remains a diff. Legacy amend retains its
required --expect interface and output. Evidence: source/tests, 2026-09-15.

The deprecated_amend CLI wrapper emits the deprecation/guidance notice on stderr
and delegates to the shared amend handler. Rewrite and internal combine calls
do not invoke the wrapper. Evidence: source and amendment tests, 2026-09-15.

The one-shot capture-review hook carries the accuracy/valid-knowledge preservation
reminder once per work cycle, rather than every rewrite success/no-op.

Mutation handlers now omit normal success/no-op receipts. The deprecated CLI
amend wrapper explicitly enables legacy output; internal combine reuse stays
silent. Access/permission changes retain consent disclosures but omit post-save
receipts. Reads/searches/inspection/previews retain requested output.


`dictionary` walks only accessible Markdown leaf path names through the existing
access-aware `leaves` iterator, strips the final .md, deduplicates components, filters segments of at most two
characters and GRAMMATICAL words, then sorts them case-insensitively for one
comma-separated output line. No leaf content is read. Optional configured root
arguments restrict the default all-accessible-root set. Evidence: tools/kt and
CLI/access integration tests, 2026-09-15.
