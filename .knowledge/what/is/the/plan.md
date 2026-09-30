---
status: green
revised_at: "2026-09-30T11:52:04+10:00"
---

Planned steps, next first. Remove a step when it is done; implementation procedure lives in `how/to/work/on/this/repository.md`.

1. Start a fresh harness against a controlled brown-root fixture and confirm proof-free startup context causes an explicit agent-side `kt_prove` call whose brown result produces a prominent priority-one incident report rather than a readiness message. Confirm no project proof command executes inside the startup hook and a proof taking longer than five seconds cannot time out startup.
2. Restart Codex, Claude Code, OpenCode, and Copilot CLI so they load the installed 23-tool MCP server and proof-free startup hook. Exercise chained `kt_rewrite` revisions, lifecycle metadata changes, structured read/access results, `kt_audit`, `kt_register`, guarded combine, session/project access and revocation, normal elicitation, and the one-time continuation after an unavailable prompt. Confirm audit remains read-only and that current scheduler/queue/event leaves are classified without mechanical rewrites. Confirm every knowledge-tree skill appears once from `~/.agents/skills/`. Codex's unexplained `action=decline` without a visible prompt remains a client-side open issue; the continuation must prevent a forced shell workflow.
3. Observe the turn-end maintenance hook live in Codex, Copilot CLI, and OpenCode: the frontier reminder arrives, the rate limit holds, and already-maintained turns are skipped.
4. Decide whether to slim `kt info --no-prove` below Claude Code's hook-context cap.

Deferred, not scheduled: event-triggered expiry in `what/is/the/proposed/event/triggered/expiry/feature.md`.
