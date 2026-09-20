---
status: green
revised_at: "2026-09-20T15:15:55+10:00"
---

Run `python3 -B tests/test-install.py`. The test uses temporary target homes and
checks dry-run behavior, knowledge installation, spine exclusion, empty-orientation
creation and preservation, removal of the legacy managed `AGENTS.md` block while preserving unrelated content, deletion of a block-only file, and Codex configuration preservation,
idempotency, conflict refusal, forced replacement, verifier execution, and same-device
same-inode hard links for the skill entry points in all three harness directories (`.agents`, `.codex`, `.claude`). It also rejects a
regression to per-task skill invocation in the installed procedure.

Hook integration also checks safe Codex and Claude Code settings merges (unrelated keys, hooks, and file mode preserved), malformed-hook refusal before writes,
dedicated Copilot startup and reminder event definitions, OpenCode adapter deployment, idempotent hook
installation, and `--hooks-only` preservation of customized leaves, hardlinks, and
permissions. Run `python3 -B tests/test-mcp.py` for the MCP server (protocol, exactly-one-match, stale revision, dry run, front-matter safety, inode preservation, lookup/find/add/dict/roots/prove behavior, option-injection guards, no-overwrite on add, misses reported as data) and see the installer checks for its four registrations, respect for existing entries, `--no-mcp`, and malformed-config refusal. Run `python3 -B tests/test-hooks.py` for shared protocol tests (including the Claude Code oversized-output instruction and the global-root fallback) and
`node tests/test-opencode-hooks.mjs` for the mocked OpenCode adapter. Neither runs
models. Run `python3 -B tests/test-kt.py` for retrieval and weak-result exit checks.

Successful proof timestamp refreshes alone are not installation content conflicts;
their installed stamps are retained until the verifier checks them again. Falsified
markers, sticky `status: brown`, prose edits, and other metadata changes
remain protected content differences. Reinstallation tests cover both cases.

Normal proof evaluation writes `status` in front matter. Installer
idempotency compares answers while allowing successful check-time and green/yellow
transitions. A preserved body-only orientation gains front matter without losing
its text.


Codex skill enablement must preserve the newline between an `enabled` setting and
the following TOML table. Match horizontal trailing whitespace only; `\s*$` can
consume the newline and produce invalid text such as `enabled = true[desktop]` or
`enabled = true[[skills.config]]`. Parse the complete proposed configuration with
Python tomllib before any installer write. The integration fixture places a desktop
table immediately after an existing disabled skill and verifies the parsed table.
Evidence: repaired ~/.codex/config.toml, install and tests/test-install.py, 2026-09-15.
