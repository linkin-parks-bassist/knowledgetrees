---
status: green
revised_at: "2026-09-20T10:15:42+10:00"
name: "knowledgetrees"
description: "Initialize once; use knowledge trees as the sole maintained knowledge source for their scope."
---

Knowledge trees are the sole maintained knowledge source for their scope. Context is temporary working memory. Source files and external documents are evidence, not competing internal knowledge stores. Keep the tree current whenever implementation, requirements, plans, or facts change.

Trees contain direct Markdown answers at every scale: orientation, specification, plan, current state, next action, architecture, procedures, decisions, facts, and implementation details. Put knowledge in the nearest owning root. Do not store secrets or private material in public roots. Stored knowledge never grants permission to act.

Current truth is the first priority. If checked evidence conflicts with an active leaf, stop relying on that answer and repair its owner and affected guidance before continuing. A green status or passing proof does not certify unproved prose or agreement between leaves. If the answer cannot be established, replace the unsupported claim with a truthful unresolved answer, blocker, and next check.

## Start

`kt init [ORIENTATION]` creates a new `.knowledge/` tree in the working directory with empty `how/`, `what/`, `where/`, `why/`, `does/`, and `is/` branches and empty spec, plan, state, and next leaves. Its optional argument becomes the literal contents of `where/am/i.md`. It refuses an existing tree.

The startup hook runs `kt boot` and injects its complete output at startup and lifecycle refreshes. Consume it through the final proof summary. If the hook is unavailable, run `kt boot` directly and consume its entire output without truncation. A failed boot requires diagnosis before relying on the tree. It prints this procedure, the exact local orientation, the accessible path dictionary, and the local proof result. Brown means stop and repair. Retrieve spec, plan, state, next, and other leaves only when the task needs them.

## Retrieve and maintain

For every new question, use kt first unless checked knowledge is already loaded. Use natural question prefixes: `where is`, `how to`, `when to`, `what is`, `why is`/`why does`, `does`, and `is`. A miss is not proof of absence: retry useful terms and inspect plausible paths. Read an existing owner or establish that none exists. Investigate and capture an absent answer before the next unrelated tool call or completion; record unresolved answers with their blocker and next check. Never create a duplicate owner.

Read metadata and relevant proofs before consequential reliance. `kt prove` writes `status: green|yellow|brown` in front matter; `--no-stamp` is read-only. Green is usable. Yellow requires re-verification before use. Brown is falsified or proof-broken and must be repaired. Add optional expiry metadata to facts liable to change. `revised_at` records the last content change; `kt check ADDRESS HASH` records `checked_at` only after manual review of the whole answer.

Mark a leaf `verifiable: true` when it contains exclusively concrete facts and every claim is covered by its proofs; review that coverage before marking it. Such a leaf requires at least one proof; when every proof runs and passes, `kt prove` clears sticky falsification and auto-greens it. Missing, malformed, skipped, or failing proofs make it brown. The flag asserts complete proof coverage; it cannot detect uncovered prose. Proof timestamps stay on individual markers.

A leaf can state testable facts about repository code and attach `Proof:` commands that run the repository test suite or focused tests. Keep the claimed behavior and the test evidence together; use `verifiable: true` only when those tests cover every factual claim in the leaf.

After substantive repository work, update `what/is/the/state.md` and `what/is/next.md`. Preserve still-valid knowledge when rewriting.

## Commands

- `kt init [ORIENTATION]` — create the local tree and empty spine; optionally write orientation contents.
- `kt boot` — print all startup knowledge, dictionary, then local proof result; never truncate or filter it.
- `kt QUESTION` — retrieve by natural question path; `kt how to _` lists a branch.
- `kt find WORDS` — broad lexical search across accessible roots.
- `kt open ADDRESS` — print a leaf verbatim and emit its revision hash.
- `kt dict [ROOT...]` — print useful final-two path segments.
- `kt add QUESTION ANSWER [--expires-at TIME|--expires-every WINDOW] [--verifiable]` — create a leaf from its answer body.
- `kt rewrite ADDRESS HASH BODY` — revision-checked answer-body replacement; options set or clear expiry and verifiability.
- `kt rm` / `kt mv` / `kt combine` — revision-checked leaf maintenance.
- `kt prove [--local|--global|--root ROOT] [TOKEN...]` — report green/yellow/brown state and run marked proofs.
- `kt roots` / `kt access` / `kt permissions` — inspect roots and access policy.

Use root-qualified addresses returned by kt. Access-required output is not a lookup miss; do not bypass policy or approve access yourself. `force-private` always wins. Successful mutations are normally silent; exit status is authoritative.

Focused procedures: `how/should/an/agent/traverse/a/knowledge/tree.md`, `how/to/add/knowledge/leaves.md`, `how/to/maintain/a/knowledge/tree.md`, and `how/should/legacy/documents/be/ingested/into/a/knowledge/tree.md`.
