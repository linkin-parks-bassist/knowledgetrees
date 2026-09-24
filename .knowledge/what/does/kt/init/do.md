---
status: green
revised_at: "2026-09-24T10:30:29+10:00"
---

`kt init [ORIENTATION]` creates a neutral `.knowledge/` tree in the current
working directory. It creates empty `how/`, `what/`, `where/`, `why/`,
`does/`, and `is/` branches plus `where/am/i.md`. It does not create spec,
plan, state, or next-action leaves and therefore does not assume that every tree
belongs to an ongoing linear project.

Use `kt init --project [ORIENTATION]` for a repository project. It creates the
same neutral baseline and additionally creates empty `what/is/the/spec.md`,
`what/is/the/plan.md`, `what/is/the/state.md`, and `what/is/next.md`.

In either form, the optional orientation argument is written verbatim to
`where/am/i.md`; without it the file is empty. Initialization registers the new
root under `ask` without granting cross-project access and refuses to overwrite an
existing root.

`kt info` performs fresh-session startup: global procedure, exact local
orientation, dictionary, and local proof result. It does not require a local tree:
without `./.knowledge` or its `where/am/i.md`, it prints a one-line note, the
global orientation, and the global (or partial local) proof result.
