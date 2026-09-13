---
status: unverified
scope: public knowledge-tree example
source: Python kt implementation and isolated CLI integration tests
review_when: Recheck after changes to the kt CLI or root discovery.
---

Use `kt where is vivado` or `kt how to make a plan` for branch-directed lookup.
Words are consumed as directories one at a time. At the first unmatched word,
the remaining words are ranked only among leaves beneath the matched prefix.
If no candidate meets the default 60% meaningful-keyword coverage threshold,
search widens to the parent,
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

`kt roots` lists the explicit current-directory project root, the global root,
and registered roots without duplicates. Wider roots default to private; use
`kt access` for user-approved sharing. `KT_GLOBAL_ROOT` can override the global
root. Root discovery never walks parent directories; restricted roots expose no
paths or snippets.

`kt open global:how/to/add/knowledge/leaves.md` selects a global leaf explicitly;
`project:` selects the project tree. An unqualified relative path tries project
then global. Absolute Markdown leaf paths also work. Content and frontmatter are
returned verbatim. Relative paths cannot escape the selected root.

`kt prove --no-stamp leaves` checks exact semantic-component tokens in the active
root. `kt prove /path/to/project --no-stamp` selects that project's `.knowledge`;
explicit `--root ROOT` and other proof options are parsed by the built-in engine.
No separately installed verifier is required. The old standalone command is only
a compatibility entry point; new integrations use access-controlled `kt prove`. Default proof
checks may stamp outcomes; lookup and open do not verify or stamp proofs.

Default output is compact plain text for agents. Non-exact searches print one
summary (`matches=shown/total`, adequate count, selected branch where applicable,
and `coverage=lexical`), then one tab-separated line per result: root-qualified
leaf address, keyword coverage with `weak` when below threshold, leaf-review or
falsification status, and an excerpt bounded to 160 characters. Rank order is
unchanged; coverage is not confidence. Excerpts help select a leaf and are not
complete answers. Open the chosen leaf before relying on it.

Use `kt --pretty find leaves`, `kt find leaves --pretty`, or
`kt where is vivado --pretty` for the expanded human layout. Pretty mode retains
scores, longer excerpts, spacing, reminders, and terminal-only colors; `NO_COLOR`
disables colors. Default output never emits ANSI colors, including in a terminal.
Both modes preserve exact question hits and `kt open` byte-for-byte, including
frontmatter. Search modes share ordering, limits, access checks, and exit statuses.
Empty or weak-only keyword matches exit 1; blocked root access exits 3.
Results distinguish leaf-review timestamps from proof verification and retain
explicit falsification flags. Check relevant proofs before reliance.
The installer puts the script in the global `.tools/kt` and links `~/.local/bin/kt`.
