---
status: green
revised_at: "2026-09-20T15:05:36+10:00"
---

Implemented 2026-09-20: `tools/kt-mcp` is a standard-library Python stdio MCP server, installed to `~/.knowledge/.tools/kt-mcp`, that exposes the kt workflow as tools. Every write goes through the CLI, so revision conflicts, access policy, locking, proof invalidation, and inode preservation stay owned by `kt`.

- Read and edit: `kt_read` returns a leaf's revision and full text. `kt_edit` takes an address, the read revision, exact `old_text`, and `new_text` (optional `dry_run`); `old_text` must match exactly once in the answer body, a stale revision or restricted access writes nothing, and it returns a diff plus the new revision. `kt_rewrite` replaces a whole answer body and is kept separate.
- Retrieve: `kt_lookup` takes a natural question (`how to ...`, `where is ...`, and the other prefixes; `how to _` lists a branch). `kt_find` searches all accessible roots (optional `limit`). `kt_dict` and `kt_roots` print the dictionary and root policy. A miss or brown result is returned as data with `(exit 1)`; only exit 2 or higher is a tool error.
- Create and check: `kt_add` creates a leaf from a question and answer (scope local or global; unresolved/blocker/next_check, expiry, `verifiable`, and `dry_run` supported) and refuses to overwrite an existing owner. `kt_prove` reports green/yellow/brown and is read-only unless `stamp` is set.
- Not exposed: `rm`, `mv`, `combine`, `register`, `access`, and `permissions`, because they are destructive or change access policy.

Arguments are passed after `--` and words starting with `-` are rejected, so no input can inject a CLI option; the CLI never reads the protocol stream (stdin is closed for it). Lookup words and search terms are split on whitespace.

`./install` registers the server: Codex `[mcp_servers.knowledgetrees]` in `~/.codex/config.toml`, OpenCode `mcp.knowledgetrees` in `opencode.json`, Copilot CLI `mcpServers.knowledgetrees` in `~/.copilot/mcp-config.json`, and Claude Code through `claude mcp add --scope user` (its own config file is never edited directly). Existing registrations under that name are left alone, other MCP servers are preserved, and `--no-mcp` skips everything. Restart each harness to load it. The server runs in the harness's working directory, so `local:` addresses resolve there; `KT_MCP_PROJECT_DIR` or `CLAUDE_PROJECT_DIR` selects the project when a user-scoped server starts elsewhere.

Verified: protocol, edit-semantics, retrieval, creation, and injection-guard tests (`tests/test-mcp.py`), installer merge tests, and a live Claude Code session that read a scratch leaf, applied an edit, and had a stale-revision retry rejected. Not yet verified live: Codex, OpenCode, and Copilot CLI invoking the tools, and the new retrieval/creation tools in any live harness; their registration formats follow each harness's documented schema. Sources: https://developers.openai.com/codex/mcp ; https://opencode.ai/docs/mcp-servers/ ; https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers ; https://code.claude.com/docs/en/mcp . Next check: call the tools through each of the other three harnesses, and `kt_lookup`/`kt_add` through Claude Code.
