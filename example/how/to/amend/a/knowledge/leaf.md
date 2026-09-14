---
status: unverified
source: tools/kt; owner compatibility requirement, 2026-09-15
review_when: Recheck when legacy workers finish or the edit interface changes.
---

`kt amend` is deprecated in favor of `kt rewrite`. The canonical editing procedure
is `how/to/rewrite/a/knowledge/leaf.md`. Use rewrite for new work; it returns the
superseded original contents for review and restoration of still-valid knowledge.

Amend remains supported for workers that loaded the former interface. Do not
remove it until those workers have finished. Existing syntax and behavior remain:

```sh
kt open ROOT:PATH --revision
kt amend ROOT:PATH --expect HASH --body-file FILE
```

Read the leaf before amending; amend does not return its superseded contents.
HASH is the SHA-256 revision printed on stderr by open. FILE supplies complete
replacement Markdown; omit --body-file or use - for stdin. --source and --dry-run
remain available. Conflicts exit 4 without writing. Hardlinks, access controls,
review invalidation, proof handling and sticky falsification remain preserved.
