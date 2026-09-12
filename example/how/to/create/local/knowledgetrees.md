---
verified_at: '2026-09-12T13:51:10+10:00'
verified_by: codex /root
scope: public knowledge-tree example
source: sanitized adaptation of the canonical global knowledge-tree methodology
verification: Compared the procedure with the packaged skill and verifier behavior.
review_when: Recheck when root creation or verifier conventions change.
---

Create `<project>/.knowledge` when entering an active project whose reusable knowledge
belongs locally. Immediately create `how/`, `what/`, `where/`, `why/`, and
`where/am/i.md`. Repository roots also require `what/is/the/spec.md`,
`what/is/the/plan.md`, `what/is/the/state.md`, and `what/is/next.md`; use truthful
minimal or explicitly unresolved content rather than inventing answers.

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
and run `~/.knowledge/.tools/verify-knowledgetree-proofs` from the project before
relying on the new tree. Before installation, this repository's packaged verifier
can be run as `tools/verify-knowledgetree-proofs`.
