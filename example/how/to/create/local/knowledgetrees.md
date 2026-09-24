---
status: green
revised_at: "2026-09-24T10:30:43+10:00"
---

Run `kt init [ORIENTATION]` from any directory to create a neutral local
knowledge tree. It creates `how/`, `what/`, `where/`, `why/`, `does/`,
`is/`, and `where/am/i.md` without assuming that the scope is an ongoing
linear project. The optional argument supplies literal `where/am/i.md` contents.
It registers the created tree under `ask` for cross-project discovery without
granting access elsewhere and refuses to overwrite an existing tree.

Run `kt init --project [ORIENTATION]` when initializing a repository project.
That opt-in creates the same baseline plus empty
`what/is/the/spec.md`, `what/is/the/plan.md`,
`what/is/the/state.md`, and `what/is/next.md`. Replace those placeholders
with truthful minimal or explicitly unresolved current answers rather than
inventing requirements, progress, or priorities.

The same neutral convention applies in any directory, including repository
subfolders. Create narrower roots when a subsystem has useful local context;
consult that root before broader roots and verify it when entering the scope.
Keep shared facts at their broader owner and subsystem-specific facts locally so
directory scope filters irrelevant context before semantic retrieval begins.

Before creating any other leaf, write the full natural-language question it
answers, lowercase it, remove only non-semantic punctuation, replace every space
with `/`, and add `.md` to the last word. The resulting path should read
roughly as the full question when slashes are spoken as spaces.

Every payload file in `.knowledge` must be a Markdown leaf. Keep scripts, JSON,
images, caches, manifests, copied sources, and other implementation artifacts in
their owning repositories, not in the tree. Do not initialize a nested Git
repository inside a project tree.

Store build, test, current-state, and subsystem knowledge locally; keep
host-wide personal tooling knowledge in `~/.knowledge`. Read ancestor
instructions first, commit local knowledge with related project changes under
that repository's policy, and run `kt prove` from the project before relying on
the new tree. Before installation, this repository's packaged verifier can be
run as `tools/kt prove`.
