---
status: "green"
revised_at: "2026-09-24T10:39:15+10:00"
---

The operational project tree is `.knowledge/`; `example/` is the public distributable corpus and keeps an empty orientation for adopters. The repository contains the self-contained `tools/kt` CLI, startup adapters for Claude Code, Codex, OpenCode, and Copilot CLI, the `tools/kt-mcp` server, installer, integration tests, README, and public guidance. Repository-specific requirements and progress stay in this tree.

The installed CLI and MCP server match this checkout. The MCP server exposes 23 tools. It includes revision-guarded whole-leaf rewrite, exact edit and undo, add/remove/move/combine, initialization and ask-only registration, dictionary/search/read/status/proof operations, arbitrary approved-root targeting for add/status/prove, and access status/request/confirm/revoke. Combine requires every source revision, handles destination revisions, and rejects duplicate aliases. Direct access-policy administration and the persistent permissions bypass remain terminal-only.

Access approval normally uses MCP elicitation. If elicitation is absent, cancelled, declined without a verifiable prompt, invalid, or errors, no policy changes and the server returns a one-time pending request. Only explicit conversational authorization for that exact root and scope permits `kt_access_confirm`; unknown, reused, wrong-kind, changed-project, denied, and force-private requests fail. Current-project revocation is direct. Wider revocation uses elicitation or a matching one-time repeat-call continuation after explicit authorization. Access registrations and grants remain path-keyed; dead-tree project grants, everywhere allows, and auto-named ask registrations are pruned, while deny, force-private, and user-named ask entries are retained.

The installer preserves personal orientation, unrelated configuration and access policy, deploys only startup hook events, registers the MCP server with all four harnesses, removes its obsolete managed home `AGENTS.md` block, and hardlinks compatibility skills into the shared skill catalog. `KT_MCP_PROJECT_DIR` or `CLAUDE_PROJECT_DIR` selects the project when a user-scoped MCP server starts elsewhere. Claude Code receives an instruction to call `kt_info` when startup output exceeds its 9,500-byte hook limit. Harnesses must restart to load the 23-tool server.

The canonical current-truth guidance now requires an affected-owner inventory and both positive and negative semantic searches before a change may be called destaled. Tests, green proofs, current timestamps, and zero installed-byte drift are supporting checks, not substitutes for reading every affected owner. Brown is now an explicit priority-one incident and mandatory stop condition even at idle startup: the agent's first response must report the affected leaf, then work is limited to diagnosis, remediation, and re-checking unless the user explicitly permits ignoring that specific status. The central procedure, focused maintenance/traversal/proof guidance, lifecycle answer, README, CLI notices, MCP instructions, repository spec and plan, public example, installed global leaves, and skill hardlinks carry that policy. A neutral readiness response to a brown startup tree is explicitly noncompliant.

Proof markers are now timeless exact `Proof:` delimiters. Proof execution stores no
per-proof outcome or timestamp and may write only leaf lifecycle status; manual
whole-leaf review time remains `checked_at`. A writing `kt prove` accepts former
`(verified|falsified at …)` markers, including `_`, solely as migration input and
silently normalizes them to `Proof:` without parsing their timestamp text.
`--no-stamp` accepts the same legacy forms while remaining byte-for-byte read-only.
The CLI, installer comparison, sync comparison, README, public guidance, local
semantic owners, installed guidance, and regression coverage use this contract.

Every non-empty kt CLI stdout and stderr stream now terminates with a newline.
Whole-leaf reads preserve complete content but append a presentation-only newline
when stored bytes lack one; revision hashes still cover the stored bytes. Neutral
`kt init [ORIENTATION]` creates only the six canonical branches and
`where/am/i.md`. `kt init --project [ORIENTATION]` opts into empty spec, plan,
state, and next placeholders, and MCP `kt_init` exposes the same choice as
`project: true`. Focused CLI and MCP tests cover both initialization modes, the
schema, refusal behavior, and newline termination.

All Python integration suites and the OpenCode adapter suite pass. Focused MCP coverage exercises all 23 tools, schemas and annotations, combine aliases and staleness, arbitrary-root operations, grant continuations, wider-revocation continuations, and refusal paths. Local, public-example, and installed-global proof sweeps have zero yellow and brown leaves; installed instruction sync has zero drift; installed `kt` and `kt-mcp` are byte-identical to the checkout; Git whitespace and public-content scans pass. These checks establish repository behavior, not live client rendering.

The remaining qualification work is live-harness observation after restart: the original MCP operations were observed in Claude Code, and older Codex/OpenCode sessions exercised earlier tool sets, but the complete 23-tool build and the new continuation paths have not yet been observed across all four freshly restarted harnesses. Codex has previously advertised elicitation while returning `action=decline` without displaying a prompt; the cause remains client-side and unresolved, but the MCP-native continuation prevents it from forcing a shell workflow. Copilot CLI remains unobserved live. The proposed event-triggered expiry feature remains deferred.
