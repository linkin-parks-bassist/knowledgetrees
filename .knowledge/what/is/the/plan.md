---
status: green
revised_at: "2026-09-27T14:50:05+10:00"
---

Planned steps, next first. Remove a step when it is done; how to carry out a change is in `how/to/work/on/this/repository.md`.

1. Start a fresh harness against a controlled brown-root fixture and confirm its first response is a prominent priority-one incident report rather than a readiness message.
2. Restart Codex, Claude Code, OpenCode, and Copilot CLI so they load the installed 22-tool MCP server, then exercise `kt_register`, revision-guarded `kt_combine`, a normal `kt_access_request` elicitation, the one-time `kt_access_confirm` continuation after a deliberately unavailable or unrendered prompt, and the matching `kt_access_revoke` continuation for wider revocation. Confirm each knowledge-tree skill appears once from `~/.agents/skills/`. Open issue: Codex has advertised elicitation while returning `action=decline` without showing a prompt; the cause is client-side and unresolved, and the continuation keeps it from forcing a shell workflow.
3. Observe the turn-end maintenance hook live in Codex (`Stop`), Copilot CLI (`agentStop` with `decision: block`), and OpenCode (`session.idle` follow-up prompt): the reminder arrives, the five-minute rate limit holds, and self-maintained turns are skipped.
4. Decide whether to slim `kt info` below Claude Code's 9,500-byte hook cap.

Deferred, not scheduled: the event-triggered expiry idea in `what/is/the/proposed/event/triggered/expiry/feature.md`.
