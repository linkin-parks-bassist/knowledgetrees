---
verified_at: '2026-09-12T20:06:26+10:00'
verified_by: codex /root
scope: public knowledge-tree example
source: Python kt implementation and isolated CLI integration tests
verification: Checked phrase ranking, root precedence, metadata, verbatim reads, and verifier argument forwarding.
review_when: Recheck after changes to the kt CLI or root discovery.
---

Use `kt find leaves` for quick ranked keyword lookup, or pass a quoted question:
`kt find "how to add knowledge leaves"`. Words are matched case-insensitively;
question-shaped paths receive higher scores than body matches. This is lexical
retrieval, not a semantic model, and scores are not probabilities of correctness.
A no-match result exits 1 but does not establish that knowledge is absent.

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
