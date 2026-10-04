---
status: green
revised_at: "2026-10-05T00:14:25+11:00"
---

`kt_rewrite` is the only editing method. First read the complete leaf with `kt_read` or an exact
`kt_lookup`; there are no partial reads in MCP or kt. The read returns the answer plus a final `Revision:` SHA-256
line and no other metadata. Pass that hash and the complete replacement answer to `kt_rewrite`. A stale hash fails
under the CLI's locked revision check. There is no partial edit: every change rewrites the whole answer, so its full contents are reconsidered each time. Keep leaves short enough to rewrite whole.
`kt_undo` reverses the latest rewrite while the answer remains unchanged.
Every full shell leaf read supplies `Revision: HASH` on stderr for the stored
bytes. Stdout returns the complete content and adds a presentation-only trailing
newline when those bytes lack one. Ranked excerpts are not full reads and do not
supply a revision for editing.

Successful `kt_rewrite` calls return the answer diff followed by `Revision: HASH`, including unchanged no-ops. Reuse that committed hash for the next rewrite without reading back the answer already in context. Dry runs return only a preview and no new revision. The CLI supplies the committed hash under the write lock via `--print-revision`; MCP remembers the supplied whole answer for renewal and undo without a post-write read. If another writer changes the leaf, the next rewrite rejects the stale hash; reread and merge then. Renewal still requires verification of the whole answer, but no redundant read after a successful rewrite.

Growth beyond 500 words requires one rejection, beyond 1,000 two, and beyond 2,000 three; severity uses the larger current/proposed body. During a cycle, long replacements that do not shrink consume the remaining rejections; after exhaustion they can pass. Answers of at most 500 words or shorter than the committed body pass immediately. Count whitespace-separated answer-body words, excluding generated metadata. Rejections preserve the leaf and revision. Remove stale, irrelevant, or log-shaped content while preserving valid knowledge. Consider splitting independently useful content into separate leaves; keep cohesive knowledge together. Reconsider the whole answer before retrying; identical retries cannot demonstrate review. Length is a pressure signal, not a diagnosis.

The CLI exits 5 for a length bounce; MCP returns a tool error and records no undo entry. Counts persist across calls and process restarts in `rewrite-bounces.sqlite3` under `$XDG_STATE_HOME/knowledgetrees` (default `~/.local/state/knowledgetrees`), outside tree payloads; `KT_REWRITE_STATE_DIR` overrides its directory. Counts are keyed by device/inode and committed revision, so hardlinks share a cycle and changed revisions start fresh. Accepted body rewrites clear their cycle. Dry runs, stale or invalid requests, unchanged no-ops, and metadata-only changes consume no bounces.

In the shell, use the canonical editing command:

```sh
kt rewrite ROOT:PATH HASH "Complete revised answer body"
```

HASH is a mandatory positional SHA-256 revision from a whole read or successful rewrite. There is no
rewrite --expect option. A matching hash establishes that the leaf still has the
read contents; it does not prove how recently it was read or that the agent reviewed
it. Keep those contents in context and preserve still-valid knowledge when editing.
Contents are the complete answer body, including multiline Markdown. Do not
supply front matter. `kt` retains optional metadata and generates status and
revision time. Use `--expires-at TIMESTAMP` or `--expires-every DURATION` to set
freshness; `--no-expiry` clears it. Use `--verifiable` only after reviewing
complete proof coverage, and `--no-verifiable` to clear the flag. `kt_renew`
(`kt renew`) alone records manual `checked_at`. `--dry-run` previews the result. Quote shell
arguments correctly; operating-system argument size limits apply.

By default, shell rewrites and identical no-ops produce no stdout or stderr. With `--print-revision`, they print the committed `Revision: HASH` on stdout; dry runs never print a committed hash. Exit 0
signals success. Neither old nor new contents are echoed. --dry-run still shows
the diff, and failures report diagnostics with a nonzero exit status. Preserve
still-valid knowledge and check relevant proofs before reliance. Agent guidance
carries the accuracy/preservation requirement. A bounced rewrite requires reconsideration and another tool call; rewrites do not inject a separate
model turn; the separate, rate-limited turn-end maintenance hook may ask for one pass.

The command needs no Git repository and invokes no editor. Revision mismatch exits
4 and leaves the file untouched; reread and merge concurrent changes. An advisory
exclusive lock serializes rewrite writers, and a final content/inode check detects
ordinary intervening edits by non-locking writers. This is not transactional against
arbitrary direct file writes or power loss. In-place writes preserve hardlinks.
Access policies apply to reading and rewriting; symlink aliases cannot be rewritten.

An unchanged body with no metadata-option change is a no-op. Changed body or
optional metadata refreshes `revised_at` and keeps the leaf's `status` and
`checked_at`; `--expires-every` starts its clock at that moment. Omitted options preserve
existing expiry, verifiability, and skill entry fields. Rerun `kt prove` after
changing proofs. The exact timeless `Proof:` delimiters remain part of the answer;
rewriting never records proof outcomes or timestamps, executes proof bodies, or
claims independent whole-leaf verification.
A brown leaf stays brown, and a yellow leaf yellow, through a rewrite until an independent whole-leaf
review is recorded with `kt_renew`, or complete eligible proofs pass on a
`verifiable: true` leaf.

Evidence: the rewrite integration test uses a standalone non-Git tree and verifies conflict
refusal, dry-run/no-op behavior, in-place hardlinks, status and check-time preservation, timeless
proof-marker preservation, sticky falsification, body-only text, input validation,
symlink refusal, denied-root behavior, growth severity, persisted counters, hardlink aliases, shrinking replacements, revision resets, and bounce-free previews/no-ops/metadata changes. Existing lookup and access tests pass.
