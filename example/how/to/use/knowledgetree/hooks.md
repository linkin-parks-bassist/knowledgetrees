---
status: green
revised_at: "2026-09-21T14:30:56+10:00"
---

Install startup-only knowledge-tree context with the knowledge-tree installer. For an
existing root, use `./install --hooks-only --force` to update infrastructure while
preserving leaves and hardlinked skills. Preview first with `--dry-run`. The same
run deploys and registers the MCP server unless `--no-mcp` is given.

The shared Python startup handler lives at `~/.knowledge/.tools/kt-hooks`. Claude
Code definitions merge into `~/.claude/settings.json`; Codex definitions merge into
`~/.codex/hooks.json`; OpenCode loads
`~/.config/opencode/plugins/knowledgetrees.js`; Copilot CLI loads
`~/.copilot/hooks/knowledgetrees.json`. Unrelated hooks remain intact. Reinstalling
removes this project's formerly managed prompt, post-tool, failure, stop, and idle
hooks while preserving unrelated definitions. The dedicated Copilot and OpenCode
adapters are rewritten as startup-only adapters.

The installed handler is executable.

Proof: (verified at _)

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

Non-startup knowledge-tree hooks are deliberately disabled. No managed hook watches
prompts or tool results, applies failure heuristics, counts calls, requests a capture
review, blocks task completion, or creates an extra model turn. The MCP tools and
normal agent instructions provide lookup and capture directly. The shared handler
may retain dormant compatibility code, but the installed harness definitions and
OpenCode adapter do not invoke it.

Review Claude Code and Codex definitions with `/hooks`. Restart OpenCode and start a
fresh Copilot CLI session after updating adapters. Startup always uses the exact
current-directory root and normal access policy; it never searches parent
directories or widens access.

Source: `tools/kt-hooks`, `tools/kt-opencode.mjs`, `install`,
`tests/test-hooks.py`, `tests/test-install.py`, and
`tests/test-opencode-hooks.mjs`.
