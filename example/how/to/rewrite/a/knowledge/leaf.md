---
status: green
revised_at: "2026-09-24T10:31:43+10:00"
---

Use `kt_rewrite` as the standard editing method. First read the complete leaf with `kt_read` or an exact
`kt_lookup`; there are no partial reads in MCP or kt. The read returns the answer plus a final `Revision:` SHA-256
line and no other metadata. Pass that hash and the complete replacement answer to `kt_rewrite`. A stale hash fails
under the CLI's locked revision check. Use `kt_edit` only for economy when making a tiny surgical exact-match replacement after a whole read;
`kt_undo` reverses the latest rewrite or edit while the answer remains unchanged.
Every full shell leaf read supplies `Revision: HASH` on stderr for the stored
bytes. Stdout returns the complete content and adds a presentation-only trailing
newline when those bytes lack one. Ranked excerpts are not full reads and do not
supply a revision for editing.

In the shell, use the canonical editing command:

```sh
kt rewrite ROOT:PATH HASH "Complete revised answer body"
```

HASH is a mandatory positional SHA-256 revision from the read. There is no
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

Successful rewrites and identical no-ops produce no stdout or stderr. Exit 0
signals success. Neither old nor new contents are echoed. --dry-run still shows
the diff, and failures report diagnostics with a nonzero exit status. Preserve
still-valid knowledge and check relevant proofs before reliance. Agent guidance
carries the accuracy/preservation requirement; no task-end reminder hook is active or
installed and rewrites do not create an extra model turn.

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
