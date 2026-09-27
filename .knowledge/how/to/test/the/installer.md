---
status: green
revised_at: "2026-09-27T14:38:54+10:00"
---

Run `python3 -B tests/test-install.py`. It uses temporary target homes and checks dry-run and consent behavior, knowledge installation, orientation preservation, legacy `AGENTS.md` cleanup, configuration merging, idempotency, conflict refusal, forced replacement, proof execution, and hardlink identity. Knowledge-tree skill entry points must exist in the shared `.agents` catalog and Claude Code's `.claude` catalog; Codex-local copies and their exact explicit registrations must be absent. The test also runs `sync-kt-instructions.py` against the temporary home to ensure instruction refresh cannot recreate retired Codex-local copies.

Hook integration verifies the startup and turn-end maintenance definitions (Claude Code and Codex `SessionStart`/`Stop`, Copilot `sessionStart`/`agentStop`, and the OpenCode plugin) while preserving unrelated hooks, keys, and file modes and refusing malformed configuration before writes. It checks that reinstalling neither duplicates managed `Stop` entries nor keeps formerly managed prompt, post-tool, and failure hooks. `--hooks-only` preserves customized leaves, hardlinks, registrations, and permissions.

Run `python3 -B tests/test-mcp.py` for all exposed MCP tools, including whole reads with revision hashes, required read-before-rewrite behavior, stale-hash rejection, tiny exact edits, undo, renew, access elicitation, and `kt_rm`, `kt_mv`, and `kt_init`. Run `python3 -B tests/test-hooks.py` for shared startup and maintenance protocol behavior (rate limit, continuation passes, and already-maintained detection from Claude Code and Codex transcript fixtures), `node tests/test-opencode-hooks.mjs` for the OpenCode adapter (including idle maintenance delivery and per-turn call tracking), `python3 -B tests/test-grants.py` for access lifecycle, `python3 -B tests/test-kt.py` for retrieval, and `python3 -B tests/test-grep-status.py` for grep and status. These tests do not run models.

Installer comparisons treat proof markers as exact, timeless answer content and tolerate only expected green/yellow lifecycle status transitions; sticky brown status, prose edits, markers, and other meaningful metadata differences remain protected. Codex TOML changes are parsed before write, and skill-registration cleanup preserves unrelated tables and settings.
