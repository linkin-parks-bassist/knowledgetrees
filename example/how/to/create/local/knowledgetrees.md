---
status: unverified
scope: public knowledge-tree example
source: sanitized adaptation of the canonical global knowledge-tree methodology
review_when: Recheck when root creation or verifier conventions change.
---

Create `<project>/.knowledge` when entering an active project whose reusable knowledge
belongs locally. Immediately create `how/`, `what/`, `where/`, `why/`, `does/`, `is/`, and
`where/am/i.md`. Repository roots also require `what/is/the/spec.md`,
`what/is/the/plan.md`, `what/is/the/state.md`, and `what/is/next.md`; use truthful
minimal or explicitly unresolved content rather than inventing answers.

The same convention applies in any directory, including repository subfolders.
Create narrower roots when a subsystem has useful local context; consult that root
before ancestor roots and verify it when entering the scope. Keep shared facts at
their broader owner and subsystem-specific facts locally so directory scope filters
irrelevant context before semantic retrieval begins.

Before creating any other leaf, write the full natural-language question it answers,
lowercase it, remove only non-semantic punctuation, replace every space with `/`,
and add `.md` to the last word. The resulting path should read roughly as the full
question when slashes are spoken as spaces.

Every payload file in `.knowledge` must be a Markdown leaf. Keep scripts, JSON,
images, caches, manifests, copied sources, and other implementation artifacts in
their owning repositories, not in the tree. Do not initialize a nested Git repository
inside a project tree.

Store build, test, current-state, and subsystem knowledge locally; keep host-wide
personal tooling knowledge in `~/.knowledge`. Read ancestor instructions first,
commit local knowledge with related project changes under that repository's policy,
and run `kt prove` from the project before
relying on the new tree. Before installation, this repository's packaged verifier
can be run as `tools/kt prove`.
