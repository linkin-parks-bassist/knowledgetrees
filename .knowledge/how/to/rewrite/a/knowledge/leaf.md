---
status: green
revised_at: "2026-09-21T14:45:59+10:00"
---

Agents use `kt_rewrite` as the standard editing tool: first use `kt_read` or an exact lookup, which returns the complete answer plus its `Revision: HASH` and no other metadata, then pass that hash with the complete replacement answer. Neither MCP nor kt has partial leaf reads. Ranked excerpts are selectors, not reads, and supply no hash. The locked CLI rejects stale hashes. Use `kt_edit` only for economy when making a tiny surgical exact-match change after a whole read; the shell command below has the same whole-answer contract.

Use the canonical editing command:

```sh
kt rewrite ROOT:PATH HASH "Complete revised answer body"
```

HASH is a mandatory positional SHA-256 revision from the read. There is no
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

Successful rewrites and identical no-ops produce no stdout or stderr. Exit 0
signals success. Neither old nor new contents are echoed. --dry-run still shows
the diff, and failures report diagnostics with a nonzero exit status. Preserve
still-valid knowledge and check relevant proofs before reliance. Agent guidance carries the accuracy/preservation requirement. No task-end reminder hook is installed, and rewrites do not create an extra model turn.

The command needs no Git repository and invokes no editor. Revision mismatch exits
4 and leaves the file untouched; reread and merge concurrent changes. An advisory
exclusive lock serializes rewrite writers, and a final content/inode check detects
ordinary intervening edits by non-locking writers. This is not transactional against
arbitrary direct file writes or power loss. In-place writes preserve hardlinks.
Access policies apply to reading and rewriting; symlink aliases cannot be rewritten.

An unchanged body with no metadata-option change is a no-op. Changed body or
optional metadata refreshes `revised_at` and keeps the leaf's `status` and
`checked_at` (`--expires-every` starts its clock at that moment). An unchanged assertion-paragraph
plus fenced predicate retains its original proof marker. New or changed proofs
are reset to `Proof: (verified at _)` and must be checked separately. Rewriting
never executes proof bodies or claims independent whole-leaf verification.
A brown leaf stays brown, and a yellow leaf yellow, through a rewrite until an independent whole-leaf
review is recorded with `kt renew`, or complete eligible proofs pass on a
`verifiable: true` leaf.

Evidence: the rewrite integration test uses a standalone non-Git tree and verifies conflict
refusal, dry-run/no-op behavior, in-place hardlinks, status and check-time preservation, unchanged
and changed proof stamps, sticky falsification, body-only text, input validation,
symlink refusal, and denied-root behavior. Existing lookup and access tests pass.
