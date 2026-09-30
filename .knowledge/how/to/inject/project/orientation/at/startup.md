---
status: green
revised_at: "2026-09-30T11:52:03+10:00"
---

Claude Code and Codex SessionStart, OpenCode system-context startup, and Copilot CLI sessionStart run `kt --lean info --no-prove` in the exact working directory. They inject the complete proof-free output: canonical global procedure, every accessible ancestor orientation from `~` down to the working directory in descending order, and dictionary. Access is evaluated from the working directory; inaccessible ancestor trees are skipped, and presenting an ancestor does not add it to lookup.

The startup context explicitly requires the agent to run `kt_prove` for the exact local root (shell fallback: `kt prove --local`), or for the global root when no exact local tree exists, before other work. Project proof commands therefore execute visibly through normal agent tooling and permissions, never inside the startup hook. The hook itself remains bounded even when proofs are slow, interactive, or unsafe.

Claude Code instead injects an instruction to call `kt_info`, or run `kt info` without tools, when the context exceeds its roughly 10,000-character hook limit (9,500 bytes in the handler). Direct `kt info` includes its proof result. An exact local tree without `where/am/i.md` is noted; if no accessible ancestor orientation exists, startup falls back to the global orientation. A genuine information-loading failure is reported in context.
