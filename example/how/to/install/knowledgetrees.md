---
status: green
revised_at: "2026-09-20T15:15:54+10:00"
---

From a complete repository checkout, run `./install`. Preview the targets without
writing with `./install --dry-run`. The installer merges reusable example leaves
into `~/.knowledge` without installing the example's illustrative spine, preserves
an existing `where/am/i.md`, installs the unified CLI at
`~/.knowledge/.tools/kt` (including `kt prove`), installs startup hooks for Claude Code, Codex, OpenCode, and Copilot CLI, and deploys a local MCP server registered with all four (skip it with `--no-mcp`). The installer removes its legacy managed block from `~/AGENTS.md`; if that was the whole file, it deletes the file. Other contents are preserved.

For a new root, it seeds truthful generic navigation in `where/am/i.md`; add
verified local environment facts. Before any writes, OpenCode configuration changes
require informed `[n/Y]` consent: reads of `~/.knowledge/**` and `~/.agents/**`,
writes to `~/.knowledge/**`, and possible model-provider exposure are disclosed.
Edits to `.agents/**` remain approval-gated. Declining or EOF cancels without changes.
Read `how/to/allow/knowledge-tree/access/in/opencode.md` for permission semantics.

Startup hooks inject the complete `kt info` output once for a fresh session; Claude Code, which drops hook context past roughly 10,000 characters, instead receives an instruction to run `kt info` directly when the output is larger. The loaded procedure remains active across messages, turns, and tasks; it is not reloaded for each task. Compatibility skills remain available if a hook is unavailable.

The installer retains a skill-shaped entry point for compatibility and explicit fallback. It creates
`~/.agents/skills/knowledgetrees/SKILL.md`,
`~/.codex/skills/knowledgetrees/SKILL.md`, and
`~/.claude/skills/knowledgetrees/SKILL.md` as hard links to the canonical installed
leaf at `~/.knowledge/how/to/use/knowledgetrees.md`. It also enables the Codex entry
in `~/.codex/config.toml`. The four paths share one inode, so editing the canonical
leaf cannot leave a wrapper or copied skill body stale.

Four procedure skills are also installed in each of those directories:
`knowledgetrees-lookup`, `knowledgetrees-capture`, `knowledgetrees-maintenance`,
and `knowledgetrees-ingestion`. Each hardlinks to the respective retrieval,
capture, maintenance, or ingestion leaf, with discovery metadata in that canonical
leaf. All five skills are enabled in Codex configuration and OpenCode permissions.
Quit and restart clients after installation or updates to refresh hooks and catalogs.

The installer also deploys the MCP server `~/.knowledge/.tools/kt-mcp` and registers it: Codex in `~/.codex/config.toml`, OpenCode under `mcp` in `opencode.json`, Copilot CLI in `~/.copilot/mcp-config.json`, and Claude Code through `claude mcp add --scope user` (printed as a manual command when the `claude` CLI is absent). Existing `knowledgetrees` registrations and other servers are left alone. The OpenCode entry is added without a separate prompt, under the write access the `[n/Y]` consent already discloses. `--hooks-only` refreshes it too. See `how/to/expose/structured/knowledge-tree/edits/across/local/agent/harnesses.md`.

Installation is idempotent when installed content is unchanged. Differing existing
leaves or bootstrap skill bodies cause a preflight failure; inspect the differences
before using `--force`. The orientation leaf is preserved even with `--force`.
Hard links require the relevant destinations to be on the same filesystem.
