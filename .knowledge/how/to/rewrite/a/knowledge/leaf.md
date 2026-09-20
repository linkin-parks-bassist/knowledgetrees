---
status: green
revised_at: "2026-09-21T09:03:53+10:00"
---

Agents change a leaf with the `kt_edit` tool (exact-match replacement after a whole read); the shell command below replaces a whole answer. Read a leaf normally with `kt open ROOT:PATH` or an exact sentence-prefix query.
Every full leaf read supplies `Revision: HASH` on stderr for the same bytes returned
verbatim on stdout. Ranked excerpts are not full reads and do not supply a
revision for editing.

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
still-valid knowledge and check relevant proofs before reliance. The existing
one-shot task-end capture-review hook carries the accuracy/preservation reminder
once per work cycle, rather than repeating it after every rewrite.

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
