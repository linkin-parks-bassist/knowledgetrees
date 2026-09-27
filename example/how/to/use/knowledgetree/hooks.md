---
status: green
revised_at: "2026-09-27T14:38:17+10:00"
---

Install startup context and turn-end maintenance reminders with the knowledge-tree
installer. For an existing root, use `./install --hooks-only --force` to update
infrastructure while preserving leaves and hardlinked skills. Preview first with
`--dry-run`. The same run deploys and registers the MCP server unless `--no-mcp` is
given.

The shared Python handler lives at `~/.knowledge/.tools/kt-hooks`. Claude Code
definitions (`SessionStart`, `Stop`) merge into `~/.claude/settings.json`; Codex
definitions (`SessionStart`, `Stop`) merge into `~/.codex/hooks.json`; OpenCode loads
`~/.config/opencode/plugins/knowledgetrees.js`; Copilot CLI loads
`~/.copilot/hooks/knowledgetrees.json` (`sessionStart`, `agentStop`). Unrelated hooks
remain intact and reinstalling never duplicates a managed definition. Reinstalling
removes this project's formerly managed prompt, post-tool, and failure hooks while
preserving unrelated definitions.

The installed handler is executable.

Proof:

```sh
test -x "$HOME/.knowledge/.tools/kt-hooks"
```

## Startup behavior

Claude Code and Codex `SessionStart`, OpenCode system-context initialization, and
Copilot CLI `sessionStart` run `kt --lean info` in the exact working directory and
inject its complete output: canonical procedure, exact local orientation,
dictionary, and proof result. Resume, clear, and compact lifecycle sources count as
startup refreshes where the harness supports them. A missing local tree falls back
to the global root. A genuinely failed `kt info` is reported in context and must be
diagnosed before the tree is trusted.

Claude Code caps injected hook context near 10,000 characters. Above 9,500 bytes
(configurable with `KT_HOOK_CONTEXT_LIMIT`), its startup hook tells the agent to
call `kt_info` or run `kt info` without tools and consume the complete output. Other
harnesses receive the full injection. Codex startup text also reminds agents that
MCP tool names may be prefixed `mcp__knowledgetrees__kt_`.

## Turn-end maintenance

When an agent finishes a turn, Claude Code and Codex `Stop`, Copilot CLI
`agentStop`, and OpenCode `session.idle` may ask for one maintenance pass: invoke the
`knowledgetrees-maintenance` skill for each tree touched by the work, user direction,
or decisions since the last pass, update leaves whose answers changed, capture new
leaf-worthy knowledge (including user guidance) at its owning scope, and
rewrite or remove leaves that can no longer be accurate or relevant; if nothing
changed, say so in one line and finish. Claude Code, Codex, and Copilot receive
`decision: block` with the reminder as its reason; the OpenCode plugin sends it as a
synthetic follow-up prompt with the session's last agent and model.

A turn gets no reminder when either of these holds:

- **Rate limit:** the session was reminded, or maintained the tree unprompted, less
  than `KT_HOOK_MAINTENANCE_INTERVAL` seconds ago (default 300, so at most one
  reminder per five minutes per session). Skipped turns are covered by the next
  reminder, which asks about everything since the last pass. Direction-only turns
  with no tool calls are still reminded, because user guidance often belongs in a leaf.
- **Already maintained:** the turn wrote the tree (a `kt_rewrite`, `kt_edit`,
  `kt_add`, `kt_rm`, `kt_mv`, `kt_combine`, `kt_renew`, or `kt_undo` call under any
  MCP prefix, or a `kt rewrite|add|rm|mv|combine|renew` shell command) and made no
  code edit afterward (`Edit`, `Write`, `MultiEdit`, `NotebookEdit`, OpenCode
  `edit`/`write`/`patch`/`multiedit`, or an `apply_patch` patch). Shell commands and
  reads after the tree write do not count as edits. Claude Code and Codex turns are
  read from a bounded 4 MiB tail of the hook payload's `transcript_path`, starting at
  the last real user message (Claude Code) or `task_started` event (Codex); the
  OpenCode plugin reports the calls it saw since the last non-synthetic user message.
  Copilot has no parsed transcript, so only the rate limit applies to it.

A reminder costs one extra model turn. It never loops: Claude Code and Codex let the
stop through when `stop_hook_active` is true, and harnesses without that flag record
a pending pass per session in `~/.local/state/knowledgetrees/hooks.sqlite3` (override
with `KT_HOOK_STATE_DIR`), so the stop that ends the maintenance pass passes. A
missing session id, broken state store, or hook error fails open and lets the agent
stop; an unreadable or unrecognized transcript falls back to the rate limit alone.
Transcript formats are undocumented and may change. If OpenCode cannot deliver the
prompt, that reminder is lost and the next idle passes. The reminder grants no write permission. Claude Code behavior was
observed live; Codex `Stop`, Copilot `agentStop`, and OpenCode `session.idle`
delivery are covered by protocol and adapter tests only.

No managed hook watches prompts or tool results or applies failure heuristics. The shared handler retains dormant failure-reminder code, but the
installed harness definitions and OpenCode adapter do not invoke it.

Review Claude Code and Codex definitions with `/hooks`. Restart OpenCode and start a
fresh Copilot CLI session after updating adapters. Startup always uses the exact
current-directory root and normal access policy; it never searches parent
directories or widens access.

Source: `tools/kt-hooks`, `tools/kt-opencode.mjs`, `install`,
`tests/test-hooks.py`, `tests/test-install.py`, and
`tests/test-opencode-hooks.mjs`.
