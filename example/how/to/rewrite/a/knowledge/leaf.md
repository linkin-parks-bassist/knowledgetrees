---
status: green
revised_at: "2026-09-27T16:05:10+10:00"
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
carries the accuracy/preservation requirement. Rewrites themselves create no extra
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
symlink refusal, and denied-root behavior. Existing lookup and access tests pass.
