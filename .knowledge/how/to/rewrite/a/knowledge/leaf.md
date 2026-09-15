---
status: unverified
source: tools/kt; tests/test-amend.py
review_when: Recheck revision checks, metadata or proof handling.
---

Read a leaf normally with `kt open ROOT:PATH` or an exact sentence-prefix query.
Every full leaf read supplies `Revision: HASH` on stderr for the same bytes returned
verbatim on stdout. `open --revision` remains accepted as a compatibility flag;
it is no longer needed. Ranked excerpts are not full reads and do not supply a
revision for editing.

Use the canonical editing command:

```sh
kt rewrite ROOT:PATH HASH "Complete revised Markdown"
```

HASH is a mandatory positional SHA-256 revision from the read. There is no
rewrite --expect option. A matching hash establishes that the leaf still has the
read contents; it does not prove how recently it was read or that the agent reviewed
it. Keep those contents in context and preserve still-valid knowledge when editing.
Contents are a literal argument, including multiline Markdown. No temporary file,
stdin, editor, or extra read just to obtain a hash is required. --source records
actual evidence; --dry-run previews the diff without writing. Quote shell arguments
correctly; operating-system argument size limits apply.

Successful rewrites and identical no-ops produce no stdout or stderr. Exit 0
signals success. Neither old nor new contents are echoed. --dry-run still shows
the diff, and failures report diagnostics with a nonzero exit status. Preserve
still-valid knowledge and check relevant proofs before reliance. The existing
one-shot task-end capture-review hook carries the accuracy/preservation reminder
once per work cycle, rather than repeating it after every rewrite.

The command needs no Git repository and invokes no editor. Revision mismatch exits
4 and leaves the file untouched; reread and merge concurrent changes. An advisory
exclusive lock serializes rewrite and legacy amend writers, and a final content/inode check detects
ordinary intervening edits by non-locking writers. This is not transactional against
arbitrary direct file writes or power loss. In-place writes preserve hardlinks.
Access policies apply to reading and rewriting; symlink aliases cannot be rewritten.

Identical submissions are no-ops unless new source is supplied. Changed content
loses whole-leaf verified_at, verified_by and verification fields and becomes
unverified (or remains unresolved). updated_at records editing, not verification.
Unchanged assertion-paragraph plus fenced predicate retains its original proof
marker, regardless of any replacement timestamp supplied. New or changed proofs
are reset to `Proof: (verified at _)` and must be checked separately. Rewriting
never executes proof bodies or claims independent whole-leaf verification.
Sticky falsified_at is preserved even if omitted from the replacement; independent
review/repair remains necessary before deliberately clearing it.

Evidence: tests/test-amend.py uses a standalone non-Git tree and verifies conflict
refusal, dry-run/no-op behavior, in-place hardlinks, review invalidation, unchanged
and changed proof stamps, sticky falsification, stdin/body-only text, input validation,
symlink refusal, and denied-root behavior. Existing lookup and access tests pass.

## Deprecated compatibility command

`kt amend` is deprecated in favor of `kt rewrite`. It remains supported for living
workers that loaded the former interface; do not remove it until those workers
have finished. Its arguments, revision requirements, output and exit statuses
remain compatible. It does not return superseded contents, so read the leaf first.

```sh
kt open ROOT:PATH
kt amend ROOT:PATH --expect HASH --body-file FILE
```

Omit `--body-file` or use `-` to read complete replacement Markdown from stdin.
`--source` and `--dry-run` remain supported. New workers should use rewrite.

Legacy amend calls emit a brief deprecation notice on stderr, directing workers
to `kt open global:how/to/rewrite/a/knowledge/leaf.md` for the updated workflow.
Its existing stdout, arguments, writes and exit statuses remain unchanged.
