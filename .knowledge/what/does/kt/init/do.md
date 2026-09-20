---
status: green
revised_at: "2026-09-20T15:15:55+10:00"
---

`kt init [ORIENTATION]` creates `.knowledge/` in the current working directory. It creates empty `how/`, `what/`, `where/`, `why/`, `does/`, and `is/` branches plus `where/am/i.md` and empty spec, plan, state, and next leaves. The optional argument is written verbatim as that file's contents; without it the file is empty. It refuses to overwrite an existing root. `kt boot` performs the former fresh-session startup: global procedure, exact local orientation, dictionary, and local proof result. It does not require a local tree: without `./.knowledge` or its `where/am/i.md` it prints a one-line note, the global orientation, and the global (or partial local) proof result.
