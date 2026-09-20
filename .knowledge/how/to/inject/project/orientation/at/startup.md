---
status: green
revised_at: "2026-09-20T15:15:55+10:00"
---

Claude Code and Codex SessionStart, OpenCode system-context startup, and Copilot CLI sessionStart run `kt info` in the exact working directory and inject its complete output (Claude Code instead injects an instruction to run `kt info` directly when the output exceeds its roughly 10,000-character hook limit, 9,500 bytes in the handler): canonical global procedure, local orientation, dictionary, and local proof result. With no `./.knowledge`, or none holding `where/am/i.md`, `kt info` falls back to the global orientation and proof instead of failing; a genuinely failed `kt info` is reported in context. The hook does not search parent directories for orientation.
