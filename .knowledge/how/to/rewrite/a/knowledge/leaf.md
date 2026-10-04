---
status: green
revised_at: "2026-10-04T23:55:09+11:00"
---

Agents use `kt_rewrite` as the only editing tool: first use `kt_read` or an exact lookup, which returns the complete answer plus its `Revision: HASH` and no other metadata, then pass that hash with the complete replacement answer. Neither MCP nor kt has partial leaf reads. Ranked excerpts are selectors, not reads, and supply no hash. The locked CLI rejects stale hashes. There is no partial edit: every change rewrites the whole answer, so its full contents are reconsidered each time. Keep leaves short enough to rewrite whole. The shell command below has the same whole-answer contract.

Successful `kt_rewrite` calls return the answer diff followed by `Revision: HASH`, including unchanged no-ops. Reuse that committed hash for the next rewrite without reading back the answer already in context. Dry runs return only a preview and no new revision. The CLI supplies the committed hash under the write lock via `--print-revision`; MCP remembers the supplied whole answer for renewal and undo without a post-write read. If another writer changes the leaf, the next rewrite rejects the stale hash; reread and merge then. Renewal still requires verification of the whole answer, but no redundant read after a successful rewrite.

Growing an answer beyond 1,000 words triggers bounded reconsideration: two rejected writes, or three when the larger of the current and proposed bodies exceeds 2,000 words. During a bounce cycle, a changed answer that is still long and not shorter than the committed body uses the remaining rejections; after the budget is exhausted it can be accepted. An answer of at most 1,000 words or shorter than the committed body passes immediately. Counts use whitespace-separated answer-body words, excluding generated metadata. A rejection leaves the leaf and revision unchanged and asks you to remove stale, irrelevant, or log-shaped content while preserving still-valid knowledge. Reconsider the whole answer before retrying; identical retries cannot demonstrate review. Length is a pressure signal, not a diagnosis or a reason to delete useful knowledge.

The CLI exits 5 for a length bounce; MCP returns a tool error and records no undo entry. Counts persist across calls and process restarts in `rewrite-bounces.sqlite3` under `$XDG_STATE_HOME/knowledgetrees` (default `~/.local/state/knowledgetrees`), outside tree payloads; `KT_REWRITE_STATE_DIR` overrides its directory. Counts are keyed by device/inode and committed revision, so hardlinks share a cycle and changed revisions start fresh. Accepted body rewrites clear their cycle. Dry runs, stale or invalid requests, unchanged no-ops, and metadata-only changes consume no bounces.

Use the canonical editing command:

```sh
kt rewrite ROOT:PATH HASH "Complete revised answer body"
```

HASH is a mandatory positional SHA-256 revision from a whole read or successful rewrite. There is no
rewrite --expect option. A matching hash establishes that the leaf still has the
read contents; it does not prove how recently it was read or that the agent reviewed
it. Keep those contents in context and preserve still-valid knowledge when editing.
Contents are the complete answer body, including multiline Markdown. Do not
supply front matter; `kt` generates it. Omitted options preserve expiry,
verifiability, and skill entry fields. Use `--expires-at TIMESTAMP` or
`--expires-every DURATION` to set freshness, `--no-expiry` to clear it,
`--verifiable` after reviewing full proof coverage, and `--no-verifiable` to
clear that flag. `kt renew` alone records manual `checked_at`. Put evidence
in the answer; --dry-run previews the diff without writing. Quote shell arguments
correctly; operating-system argument size limits apply.

By default, shell rewrites and identical no-ops produce no stdout or stderr. With `--print-revision`, they print the committed `Revision: HASH` on stdout; dry runs never print a committed hash. Exit 0
signals success. Neither old nor new contents are echoed. --dry-run still shows
the diff, and failures report diagnostics with a nonzero exit status. Preserve
still-valid knowledge and check relevant proofs before reliance. Agent guidance carries the accuracy/preservation requirement. A bounced rewrite requires reconsideration and another tool call; rewrites do not inject a separate model turn; the separate, rate-limited turn-end maintenance hook may ask for one pass.

The command needs no Git repository and invokes no editor. Revision mismatch exits
4 and leaves the file untouched; reread and merge concurrent changes. An advisory
exclusive lock serializes rewrite writers, and a final content/inode check detects
ordinary intervening edits by non-locking writers. This is not transactional against
arbitrary direct file writes or power loss. In-place writes preserve hardlinks.
Access policies apply to reading and rewriting; symlink aliases cannot be rewritten.

An unchanged body with no metadata-option change is a no-op. Changed body or
optional metadata refreshes `revised_at` and keeps the leaf's `status` and
`checked_at` (`--expires-every` starts its clock at that moment). Exact, timeless `Proof:` markers remain part of the supplied answer whether their
assertion or fenced predicate changed. Rewriting never executes proof bodies,
stores proof outcomes or timestamps, or claims independent whole-leaf verification.
A brown leaf stays brown, and a yellow leaf yellow, through a rewrite until an independent whole-leaf
review is recorded with `kt renew`, or complete eligible proofs pass on a
`verifiable: true` leaf.

Evidence: the rewrite integration test uses a standalone non-Git tree and verifies conflict
refusal, dry-run/no-op behavior, in-place hardlinks, status and check-time preservation, timeless proof-marker preservation,
sticky falsification, body-only text, input validation,
symlink refusal, denied-root behavior, growth severity, persisted counters, hardlink aliases, shrinking replacements, revision resets, and bounce-free previews/no-ops/metadata changes. Existing lookup and access tests pass.
