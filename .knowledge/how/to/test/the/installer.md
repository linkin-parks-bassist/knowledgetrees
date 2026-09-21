---
status: green
revised_at: "2026-09-21T15:00:32+10:00"
---

Run `python3 -B tests/test-install.py`. It uses temporary target homes and checks dry-run and consent behavior, knowledge installation, orientation preservation, legacy `AGENTS.md` cleanup, configuration merging, idempotency, conflict refusal, forced replacement, proof execution, and hardlink identity. Knowledge-tree skill entry points must exist in the shared `.agents` catalog and Claude Code's `.claude` catalog; Codex-local copies and their exact explicit registrations must be absent. The test also runs `sync-kt-instructions.py` against the temporary home to ensure instruction refresh cannot recreate retired Codex-local copies.

Hook integration verifies startup-only definitions for Claude Code, Codex, OpenCode, and Copilot CLI while preserving unrelated hooks, keys, and file modes and refusing malformed configuration before writes. It checks that reinstalling retires formerly managed non-startup hooks. `--hooks-only` preserves customized leaves, hardlinks, registrations, and permissions.

Run `python3 -B tests/test-mcp.py` for all exposed MCP tools, including whole reads with revision hashes, required read-before-rewrite behavior, stale-hash rejection, tiny exact edits, undo, renew, access elicitation, and `kt_rm`, `kt_mv`, and `kt_init`. Run `python3 -B tests/test-hooks.py` for shared startup protocol behavior, `node tests/test-opencode-hooks.mjs` for the OpenCode adapter, `python3 -B tests/test-grants.py` for access lifecycle, `python3 -B tests/test-kt.py` for retrieval, and `python3 -B tests/test-grep-status.py` for grep and status. These tests do not run models.

Installer comparisons tolerate refreshed successful proof timestamps and green/yellow status transitions while protecting falsified markers, sticky brown status, prose edits, and other meaningful metadata differences. Codex TOML changes are parsed before write, and skill-registration cleanup preserves unrelated tables and settings.
