---
status: green
revised_at: "2026-09-20T10:27:53+10:00"
---

Future idea, not an approved implementation: let a leaf declare events that invalidate its freshness. Examples include expiring `what/is/the/state.md` after a repository commit, or expiring a code-dependent leaf when relevant code changes. The trigger would mark the leaf for manual review; it would not establish that the contents are false or update `checked_at` automatically. This could complement time-based `expires_at` and `expires_every`. Open design questions: how a leaf declares its watched paths or events, how hooks detect changes reliably across Git and non-Git trees, what status transition an event causes, and how to avoid stale green state when a hook did not run. Blocker: no behavior, syntax, or implementation has been authorized or designed. Next check: evaluate these questions if the owner chooses to prioritize event-triggered expiry. Source: owner suggestion in this conversation, 2026-09-20.
