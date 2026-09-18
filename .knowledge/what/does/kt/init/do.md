---
status: "unverified"
created_at: "2026-09-18T11:54:05+10:00"
updated_at: "2026-09-18T12:02:33+10:00"
scope: "knowledgetrees repository"
source: "Repository owner request and output-order clarification 2026-09-18; tools/kt implementation and canonical bootstrap contract"
---

`kt init` performs fresh-session startup for the exact current-directory knowledge root. It first prints labeled verbatim contents for `global:how/to/use/knowledgetrees.md`, then the local `where/am/i.md`, `what/is/the/spec.md`, `what/is/the/plan.md`, `what/is/the/state.md`, and `what/is/next.md`. It then prints the accessible path-segment dictionary and finally runs and prints `kt prove --local`, so the health check is the final output. It fails if no exact local root exists, the canonical global procedure is inaccessible, any required local startup leaf is missing, or the final proof verification is brown. Startup hooks inject only a compact instruction to run `kt init`; they do not inject procedure or orientation leaf bodies.
