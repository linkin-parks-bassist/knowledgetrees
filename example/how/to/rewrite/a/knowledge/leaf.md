---
status: unverified
source: tools/kt; tests/test-amend.py
review_when: Recheck revision checks, metadata or proof handling.
---

Use the canonical single-call editing command:

`kt rewrite ROOT:PATH "Complete revised Markdown"`. Contents are a literal argument,
including multiline text. No prior revision token, editor, stdin, or temporary file
is required. Optional `--expect HASH` rejects changes since an earlier read; without
it, replacement intentionally uses the current leaf at call time and cannot detect
stale context from before the call. Both commands detect intervening edits during
the write and share metadata, proof, hardlink, and access handling. `--source` and
`--dry-run` work with rewrite too. Use proper shell quoting when invoking through
a shell; inline arguments are subject to operating-system argument size limits.

Successful rewrite output includes the complete original contents, labeled as
superseded, followed by a reminder to check whether any still-valid knowledge
was lost and rewrite again to restore it. Review that output before continuing.
The new contents are not echoed. No-ops return the unchanged contents with an
explicit unchanged label; dry-run prints the diff and writes nothing. This review
helps preserve knowledge; the command does not automatically judge semantic loss.

If you already have a revision from `kt open ROOT:PATH --revision`, supply it as
`--expect HASH` to reject stale context. stdout from open is verbatim Markdown;
stderr supplies the SHA-256 revision of those bytes.

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
kt open ROOT:PATH --revision
kt amend ROOT:PATH --expect HASH --body-file FILE
```

Omit `--body-file` or use `-` to read complete replacement Markdown from stdin.
`--source` and `--dry-run` remain supported. New workers should use rewrite.
