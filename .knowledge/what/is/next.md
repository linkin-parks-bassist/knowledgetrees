---
status: green
revised_at: "2026-09-24T07:46:10+10:00"
---

Restart Codex, Claude Code, OpenCode, and Copilot CLI so they load the installed 23-tool MCP server. For the live demo, exercise `kt_register`, revision-guarded `kt_combine`, and both access paths: a normal `kt_access_request` elicitation, then the one-time `kt_access_confirm` continuation after a deliberately unavailable or unrendered prompt; also verify the matching `kt_access_revoke` continuation for wider revocation. Confirm each knowledge-tree skill still appears once from `~/.agents/skills/`. The underlying reason Codex previously advertised elicitation but returned decline without rendering a prompt remains a client-side investigation, but it no longer blocks the no-shell workflow. OpenCode and Copilot CLI still need live observation. Decide separately whether to slim `kt info` below Claude Code's 9,500-byte hook cap. The event-triggered expiry idea remains deferred. Repair any newly discovered stale active leaf before reliance.
