---
status: green
revised_at: "2026-09-30T11:52:04+10:00"
---

The repository ships a public, self-contained knowledge-tree system: `tools/kt`, `tools/kt-mcp`, harness hooks/adapters, an installer, regression tests, a private operational `.knowledge/` tree, and a distributable `example/` tree. The example orientation stays empty for adopters. Public content contains no private host, customer, or owner-identifying material.

## Knowledge contract

A tree is the frontier of relevant knowledge for its scope: current and only current answers, advanced in lockstep with what is known and done. A leaf is an answer, never an event stream. Rewrites recompute the complete answer; the previous body is evidence to reconsider, not a template to append to. Superseded facts, task narration, dated progress, transcripts, and obsolete mechanisms are removed. Git owns chronology. The plan contains only remaining work, next first.

Nonempty leaves use validated flat Markdown front matter. Automated fields are lifecycle status and `revised_at`; optional expiry, `checked_at`, and reviewed `verifiable` metadata follow the documented lifecycle rules. Complete-body rewrites require the SHA-256 revision from a whole read and preserve omitted metadata unless an explicit lifecycle change is requested. Stale revisions fail under the write lock. A successful rewrite returns its committed revision for another rewrite, renewal, or undo without a redundant read.

Expiry is a review trigger for volatile claims, not scheduled invalidation or a substitute for evidence. `expires_every` suits recurring review; `expires_at` suits a known temporary boundary. Architecture, rationale, specifications, plans, and proof-complete stable claims do not receive arbitrary expiry. Renewal attests that the whole answer was checked.

Green, yellow, and brown describe verification lifecycle only. Brown is a priority-one stop requiring report, diagnosis, repair, and re-check. Green does not certify unproved prose. Structural audit is separate and read-only: `kt audit` marks bodies over 1,000 words `suspect`, and bodies containing date-shaped strings `quite-suspect`. These are gardening prompts, not findings or lifecycle states. Dates that are part of current machine state, schedules, queues, event records, or protocol identifiers are legitimate and must not be rewritten merely because audit reports them.

## CLI and retrieval

The CLI is the semantic spine for discovery, access, lookup, exact whole reads, ranked search, grep, dictionary, add, complete rewrite, undo, renew, remove, move, combine, init, registration, proof, status, audit, and permissions. `kt add` is the sole creation command; the archival `capture` alias is absent. A miss requires establishing whether an owner exists, then advancing it or adding an investigated current answer before unrelated work.

Every mutation honors canonical root identity, access policy, revision locking, and force-private. `kt init` creates a neutral six-branch tree and orientation; `--project` also creates empty spec and plan leaves. Direct `kt info` prints the canonical procedure, accessible ancestor orientations, dictionary, and proof summary without turning ancestors into lookup roots. `kt info --no-prove` supplies the same startup knowledge without executing proof commands.

## MCP and access

The MCP server is a thin typed adapter over the CLI and exposes 23 tools, including `kt_audit`. It does not reimplement leaf semantics. Whole reads and exact lookups return the complete answer plus revision. Useful read and access flows also return structured content. `kt_rewrite` has CLI lifecycle parity for setting or clearing expiry and verifiability; search exposes coverage control; proof exposes timeout and verbosity.

Access defaults to least authority. Registered wider roots default to ask; deny and force-private are enforced, and force-private always wins. MCP request accepts a preferred scope and offers session scope only when a stable harness session identity exists. Project and session access can be directly relinquished; wider revocation requires user confirmation. Failed elicitation changes nothing and may yield an exact one-time continuation ID. Agents never infer approval. Persistent bypass and direct policy administration remain terminal-only.

## Maintenance and integration

Startup hooks supply proof-free `kt info --no-prove` context and require the agent to run `kt_prove` for the exact local root before other work. Hooks never execute arbitrary project proof commands. Rate-limited turn-end hooks ask agents to bring each touched tree to the frontier: reconcile affected owners, establish missing answers, inspect status and audit signals, remove stale material, and update the remaining-work plan. The continuation never edits knowledge itself and fails open.

The installer merges public guidance without overwriting orientation or project spine, deploys the CLI/MCP/hooks, preserves unrelated configuration, and creates hardlinked skills. The maintenance vocabulary is reconciliation/frontier advancement; the retired `knowledgetrees-capture` skill is removed. OpenCode permission changes require informed consent.

A change is complete only when every semantic and presentation owner is reconciled: code, tests, CLI help, MCP schemas/results, hooks, access guidance, README, public example, repository architecture/spec/plan, installed guidance, and affected global owners. Verification includes all regressions, local/example/installed proof sweeps, instruction-sync and byte-equality checks, structural audit review, public-content audit, and clean Git checks. Existing owner authorization governs publication.
