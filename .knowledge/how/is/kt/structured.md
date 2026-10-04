---
status: green
revised_at: "2026-10-05T00:09:33+11:00"
---

The implementation has one semantic spine: the self-contained standard-library `tools/kt` CLI owns root discovery, access policy, leaf representation, lifecycle, revision locking, structural audit, and proof evaluation. Harness adapters translate their protocols into that spine; they do not reimplement knowledge semantics.

## CLI layers

- Root/access functions represent registered roots, effective policies, project/session grants, and forced privacy. `RootAccessView` loads one coherent view per invocation and every traversal uses it.
- `LookupContext` lazily reads permitted leaves once. Question lookup, ranked search, exact grep, dictionary, status, and audit are read-side projections over that view.
- Leaf functions parse flat metadata and answer bodies, compute revision snapshots, lifecycle state, structural audit signals, and proof records.
- Mutation functions operate on complete current answers. `add_leaf` establishes a missing owner; `rewrite_leaf` advances an existing owner under a whole-read SHA-256 revision and preserves inode identity. Remove, move, combine, renew, and initialization share the same root and snapshot contracts.
- Proof execution is exposed only through `kt prove`. Lifecycle status and structural suspicion are distinct: green/yellow/brown describes verification state; `kt audit` reports bodies over 1,000 words as `suspect` and date-shaped bodies as `quite-suspect` without writing or diagnosing them.

The CLI has one creation route, `kt add`; the archival `capture` alias is absent. `kt rewrite` accepts the complete body plus explicit expiry/verifiability changes. The old body is input to reconsider, not a template to extend.

Growth enforcement lives in `rewrite_growth_guard`, called under the existing leaf lock after revision/input validation and before an actual body write. It applies one rejection above 500 words, two above 1,000 and three above 2,000, accepts short or shorter replacements immediately, and allows remaining legitimate growth after bounded reconsideration. Its private SQLite counters live outside knowledge payloads and are keyed by device/inode plus committed revision; hardlinks share counts. Dry runs and metadata-only/no-op writes do not consume attempts. Audit remains independently read-only; a bounce is neither a lifecycle downgrade nor a diagnosis of poisoning.

## MCP adapter

`tools/kt-mcp` is a newline-delimited JSON-RPC stdio fingertip exposing 23 typed tools. Ordinary operations run the sibling CLI with stdin closed, preserving CLI validation, access, revision, proof, and audit semantics. Read-side tools return readable text and structured content where a machine representation is useful; agents do not request a presentation format or scrape prose for access continuations.

Whole reads return the complete answer plus its revision. `kt_rewrite` returns a reusable committed revision and has parity with CLI expiry and verifiability controls. Search exposes coverage parameters; proof exposes timeout and verbosity; audit, status, roots, dictionaries, and access reports provide structured results.

Access elicitation is the deliberate protocol-owned exception. `kt_access_request` resolves policy with CLI functions, accepts an optional least-sufficient preferred scope, and offers session scope only when the harness supplies a stable session identity. Only the user-facing elicitation or an exact explicit conversational continuation can grant access. Pending grant/revocation results carry structured request IDs. Session and exact-project revocation are direct reductions of authority; wider changes require user confirmation. Deny and force-private cannot be bypassed, and direct policy administration plus the persistent permissions bypass remain terminal-only.

## Harness integration

`tools/kt-hooks` supplies startup knowledge and a rate-limited frontier-maintenance continuation to Claude Code, Codex, OpenCode, and Copilot CLI. Maintenance asks agents to recompute current answers, establish missing owners, inspect `kt_audit` signals, remove superseded facts, and leave chronology to Git. Transcript parsing only decides whether another maintenance turn is needed; it never edits knowledge.

The installer deploys the CLI, MCP server, hooks, public guidance, and hardlinked skills. The reconciliation skill is `knowledgetrees-reconcile`; the retired archival skill name is removed from shared/Claude/Codex catalogs and OpenCode permissions.

Regression suites cover access, lookup, mutation, lifecycle, audit, proofs, hooks, MCP schemas/results/elicitation, installation, and OpenCode integration. Repository guidance, public example, installed global guidance, and executables are synchronized and proved before completion.
