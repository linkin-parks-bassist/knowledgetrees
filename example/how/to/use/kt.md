---
verified_at: '2026-09-12T20:29:52+10:00'
verified_by: codex /root
scope: public knowledge-tree example
source: Python kt implementation and isolated CLI integration tests
verification: Reviewed kt-first lookup, mandatory miss classification, capture timing, retained root/proof/scope obligations, and installed hardlink identity.
review_when: Recheck after changes to the kt CLI or root discovery.
---

Use `kt where is vivado` or `kt how to make a plan` for branch-directed lookup.
Words are consumed as directories one at a time. At the first unmatched word,
the remaining words are ranked only among leaves beneath the matched prefix.
If no candidate covers at least half of those keywords, search widens to the parent,
one level at a time. This transparent lexical-coverage heuristic is not confidence
or semantic similarity. `kt where is _` lists location leaves without a query.
Exact question-path hits return full contents, frontmatter included; they do not
run proofs or establish correctness. Use `kt open` to read fallback list results.

Conventions: `where/is/` answers locations, `how/to/` procedures, `when/to/`
decision triggers, `what/is/` definitions/state, and `why/does/` or `why/is/`
rationale. Other complete question prefixes can be navigated under these starters.

Use `kt find leaves` for deliberately broad lookup, or pass a quoted question:
`kt find "how to add knowledge leaves"`. Words are matched case-insensitively;
question-shaped paths receive higher scores than body matches. This is lexical
retrieval, not a semantic model, and scores are not probabilities of correctness.
A no-match result exits 1 but does not establish that knowledge is absent.
When `kt` fails to find needed information, you MUST determine whether a leaf
exists: retry distinctive terms/synonyms and inspect plausible paths in the applicable
roots. If it exists, read or amend it; if absent, investigate and add the scoped
leaf. Preserve the established answer before the next unrelated tool call or
completion. Add a truthful unresolved record if blocked; forbidden writes require
a scoped handoff. Do not silently move on or create a duplicate from a lexical miss.

`kt roots` lists the nearest project root followed by the global root without
duplicates. `KT_GLOBAL_ROOT` can override the global root. Root discovery walks
upward for `.knowledge/where/am/i.md`; searching does not enumerate other projects.

`kt open global:how/to/add/knowledge/leaves.md` selects a global leaf explicitly;
`project:` selects the project tree. An unqualified relative path tries project
then global. Absolute Markdown leaf paths also work. Content and frontmatter are
returned verbatim. Relative paths cannot escape the selected root.

`kt proof --no-stamp leaves` checks exact semantic-component tokens in the active
root. `kt proof /path/to/project --no-stamp` selects that project's `.knowledge`;
explicit `--root ROOT` and other verifier options are forwarded. Default proof
checks may stamp outcomes; lookup and open do not verify or stamp proofs.

Results distinguish leaf-review timestamps from proof verification and highlight
leaf falsification flags. Check relevant proof evidence before relying on claims.
Colors are terminal-only; `NO_COLOR` disables them. Pipes receive plain text.
The installer puts the script in the global `.tools/kt` and links `~/.local/bin/kt`.
