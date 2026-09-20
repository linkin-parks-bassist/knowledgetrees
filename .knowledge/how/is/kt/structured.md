---
status: green
revised_at: "2026-09-21T09:03:53+10:00"
---

The CLI remains one self-contained standard-library Python executable for standalone installation. Sections separate root discovery and access, lookup and rendering, leaf maintenance, capture, proof execution, and parser construction. RootAccessView loads discovery and policies once per invocation; LookupContext lazily reads permitted leaf text once. LeafSnapshot centralizes revision and inode checks for rewrite and destructive maintenance. command_parser separates command schemas and handler dispatch from execution. All verification is exposed through kt prove. Regression suites cover access, lookup, maintenance, installation, hooks, MCP tools, and proof timestamps.

Harness adapters are separate files so the CLI stays standalone. `tools/kt-hooks` is one Python handler shared by Claude Code, Codex, Copilot CLI, and OpenCode's plugin (`tools/kt-opencode.mjs`); it runs `kt info` and keeps only hashed counters. `tools/kt-mcp` is a newline-delimited JSON-RPC stdio server that owns no policy beyond the elicitation flow (a server-to-client request whose response is read inline while a tool call is in flight; other requests arriving meanwhile are queued and served afterward, and pings are answered): each tool runs the sibling `kt` in a subprocess with stdin closed and arguments after `--`, and edits compute their replacement from the locked read revision before delegating to `kt rewrite`.

`kt grep` and `kt status` walk leaves through the same `RootAccessView`/`leaves()` policy filter as `find`, so restricted roots are never read; `status` derives colors from stored metadata and `lifecycle_state` without running proofs. Effective access is computed by `resolve_root_access`, which returns the policy plus its source and the project grant that supplied it (`root_access` is its first element); `apply_revocation` narrows a grant and can preview on a copy, `grants_command` reports sources, and `prune_stale_grants` runs once per invocation from `main` to drop approvals whose tree is gone. Access changes are split into `resolve_access_root` and `apply_access_decision`: the latter persists an already-confirmed decision and never prompts, so the CLI keeps its own-terminal confirmation while another trusted front end (the MCP server's elicitation) can supply a different confirmation. `leaf_health` computes a leaf's live state and reason once for `status` and for lean rendering (`--lean`: `lean_leaf` and `show_leaf` strip front matter and lead a non-green leaf with a notice); `renew_leaf` stamps `checked_at` and then reruns `verify_proofs` restricted to that leaf through its `only` parameter with `raise_ok`; every other proof run keeps a leaf at the worse of its computed and stored status, so proof evaluation never raises one (a `verifiable: true` leaf whose proofs all pass is the exception). `revised_leaf` carries `status` and `checked_at` through a rewrite.

`kt rewrite ADDRESS HASH BODY` uses a dedicated handler with a mandatory
positional SHA-256 revision and literal inline answer Markdown. Metadata is generated from the clock
and explicit expiry/verifiability options, preserving omitted optional fields. Full open/exact-question
reads always print the hash of the same returned bytes on stderr. Rewrite
checks the required hash against the locked snapshot
and retains final inode/content checks, hardlinks, access controls, review and
proof handling. Success and no-ops are silent (exit 0); dry-run remains a diff.
The CLI exposes rewrite as the editing command. Evidence:
source and rewrite tests, 2026-09-18.

The one-shot capture-review hook carries the accuracy/valid-knowledge preservation
reminder once per work cycle, rather than every rewrite success/no-op.

Mutation handlers omit normal success/no-op receipts. Internal combine reuse stays
silent. Access/permission changes retain consent disclosures but omit post-save
receipts. Reads/searches/inspection/previews retain requested output.


`dictionary` walks the accessible directory trees directly with `os.walk`. At each
Markdown leaf, the current directory supplies the penultimate segment and the leaf
stem supplies the final segment; it does not materialize a list of full leaf paths.
It rejects segments of at most two characters and GRAMMATICAL words before adding
candidates to the deduplicating set, then sorts the compact set case-insensitively
for one comma-separated output line. Registered nested-root directories are pruned
at traversal boundaries and walked separately only when accessible, avoiding a
per-file access-policy resolution. No leaf content is read. Optional configured root
arguments restrict the default all-accessible-root set. Evidence: tools/kt and
CLI/access integration tests, 2026-09-15.


The prove wrapper expands bare invocation into one verifier run per accessible
root and combines failure status. --local and --global select their canonical
roots before delegating to the existing verifier; --root and positional-directory
compatibility remain. Restricted registered subtrees still prevent unsafe broader
proof traversal. Evidence: tools/kt and CLI integration tests, 2026-09-15.
