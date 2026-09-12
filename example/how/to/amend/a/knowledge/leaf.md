---
status: unverified
source: tools/kt; tests/test-amend.py
review_when: Recheck revision checks, metadata or proof handling.
---

Read a leaf with `kt open ROOT:PATH --revision`. stdout remains the complete
verbatim Markdown; stderr supplies `Revision: <SHA-256>` for those same bytes.
Write a complete revised version to a temporary file and submit it with
`kt amend ROOT:PATH --expect HASH --body-file FILE`. Omit --body-file or use `-`
to read the replacement from stdin. `--dry-run` shows the resulting diff without
writing. Optional --source records actual new evidence.

The command needs no Git repository and invokes no editor. Revision mismatch exits
4 and leaves the file untouched; reread and merge concurrent changes. An advisory
exclusive lock serializes amend writers, and a final content/inode check detects
ordinary intervening edits by non-locking writers. This is not transactional against
arbitrary direct file writes or power loss. In-place writes preserve hardlinks.
Access policies apply to reading and amendment; symlink aliases cannot be amended.

Identical submissions are no-ops unless new source is supplied. Changed content
loses whole-leaf verified_at, verified_by and verification fields and becomes
unverified (or remains unresolved). updated_at records editing, not verification.
Unchanged assertion-paragraph plus fenced predicate retains its original proof
marker, regardless of any replacement timestamp supplied. New or changed proofs
are reset to `Proof: (verified at _)` and must be checked separately. Amendment
never executes proof bodies or claims independent whole-leaf verification.
Sticky falsified_at is preserved even if omitted from the replacement; independent
review/repair remains necessary before deliberately clearing it.

Evidence: tests/test-amend.py uses a standalone non-Git tree and verifies conflict
refusal, dry-run/no-op behavior, in-place hardlinks, review invalidation, unchanged
and changed proof stamps, sticky falsification, stdin/body-only text, input validation,
symlink refusal, and denied-root behavior. Existing lookup and access tests pass.
