---
status: green
revised_at: "2026-09-29T13:27:26+10:00"
---

`kt init [ORIENTATION]` creates a neutral `.knowledge/` tree in the current
working directory. It creates empty `how/`, `what/`, `where/`, `why/`,
`does/`, and `is/` branches plus `where/am/i.md`. It does not create spec
or plan leaves and therefore does not assume that every tree
belongs to an ongoing linear project.

Use `kt init --project [ORIENTATION]` for a repository project. It creates the
same neutral baseline and additionally creates empty `what/is/the/spec.md` and `what/is/the/plan.md`.

In either form, the optional orientation argument is written verbatim to
`where/am/i.md`; without it the file is empty. Initialization registers the new
root under `ask` without granting cross-project access and refuses to overwrite an
existing root.

`kt info` performs fresh-session startup: global procedure, every accessible ancestor orientation from `~` down to the working directory in descending order, dictionary, and proof result. Access is evaluated from the working directory and presentation does not add lookup roots. Without an exact local tree it proves the global root; an exact local tree without an orientation is noted and still proved. If no accessible ancestor orientation is available, it prints a one-line note and uses the global orientation.
