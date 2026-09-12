---
verified_at: '2026-09-12T20:16:19+10:00'
verified_by: codex /root
scope: public knowledge-tree example
source: Python kt implementation and isolated CLI integration tests
verification: Reviewed kt-first lookup, mandatory miss classification, capture timing, retained root/proof/scope obligations, and installed hardlink identity.
review_when: Recheck after changes to the kt CLI or root discovery.
---

Use `kt find leaves` for quick ranked keyword lookup, or pass a quoted question:
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
