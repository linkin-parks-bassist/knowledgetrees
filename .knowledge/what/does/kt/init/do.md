---
status: "unverified"
created_at: "2026-09-18T11:54:05+10:00"
updated_at: "2026-09-18T12:09:02+10:00"
scope: "knowledgetrees repository"
source: "Repository owner request and context-minimization clarification 2026-09-18; tools/kt implementation and regression coverage"
---

`kt init` performs minimal fresh-session startup. It prints labeled verbatim contents for `global:how/to/use/knowledgetrees.md` and the exact local `where/am/i.md`, then prints the accessible path-segment dictionary, and finally runs and prints `kt prove --local` so health is the last output. It does not preload spec, plan, state, next, or other task-specific leaves; retrieve those only when needed. It fails if no exact local root exists, the canonical global procedure is inaccessible, local orientation is missing, or the final proof verification is brown. Startup hooks inject only a compact instruction to run `kt init`; they inject no leaf bodies.
