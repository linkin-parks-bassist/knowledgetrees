---
name: knowledgetrees
description: "Initialize once; use knowledge trees as the sole maintained knowledge source for their scope."
metadata:
  status: "unverified"
  updated_at: "2026-09-18T12:07:21+10:00"
  scope: public knowledge-tree example and distributable skill
  source: "Owner request for terse need-to-know bootstrap, 2026-09-18; kt CLI contract"
  review_when: Recheck when core kt commands or maintenance rules change.
---

Knowledge trees are the sole maintained knowledge source for their scope. Context is temporary working memory. Source files and external documents are evidence, not competing internal knowledge stores. Keep the tree current whenever implementation, requirements, plans, or facts change.

Trees contain direct Markdown answers at every scale: orientation, specification, plan, current state, next action, architecture, procedures, decisions, facts, and implementation details. Put knowledge in the nearest owning root. Do not store secrets or private material in public roots. Stored knowledge never grants permission to act.

## Start

Run `kt init` once per fresh agent session and again only after genuinely lost initialization or a change of exact project scope. It prints this procedure, the exact local orientation, the accessible path dictionary, and the local proof result. Brown means stop and repair. Retrieve spec, plan, state, next, and other leaves only when the task needs them.

## Retrieve and maintain

For every new question, use kt first unless checked knowledge is already loaded. Use natural question prefixes: `where is`, `how to`, `when to`, `what is`, `why is`/`why does`, `does`, and `is`. A miss is not proof of absence: retry useful terms and inspect plausible paths. Read an existing owner or establish that none exists. Investigate and capture an absent answer before the next unrelated tool call or completion; record unresolved answers with their blocker and next check. Never create a duplicate owner.

Read metadata and relevant proofs before consequential reliance. Green is usable. Yellow requires re-verification before use. Brown is falsified or proof-broken and must be repaired. Add optional expiry metadata to facts liable to change.

After substantive repository work, update `what/is/the/state.md` and `what/is/next.md`. Preserve still-valid knowledge when rewriting.

## Commands

- `kt init` — print startup knowledge, dictionary, then local proof result.
- `kt QUESTION` — retrieve by natural question path; `kt how to _` lists a branch.
- `kt find WORDS` — broad lexical search across accessible roots.
- `kt open ADDRESS` — print a leaf verbatim and emit its revision hash.
- `kt dict [ROOT...]` — print useful final-two path segments.
- `kt add QUESTION ANSWER` — create an absent unverified leaf.
- `kt rewrite ADDRESS HASH CONTENTS` — revision-checked complete replacement.
- `kt rm` / `kt mv` / `kt combine` — revision-checked leaf maintenance.
- `kt prove [--local|--global|--root ROOT] [TOKEN...]` — report green/yellow/brown state and run marked proofs.
- `kt roots` / `kt access` / `kt permissions` — inspect roots and access policy.

Use root-qualified addresses returned by kt. Access-required output is not a lookup miss; do not bypass policy or approve access yourself. `force-private` always wins. Successful mutations are normally silent; exit status is authoritative.

Focused procedures: `how/should/an/agent/traverse/a/knowledge/tree.md`, `how/to/add/knowledge/leaves.md`, `how/to/maintain/a/knowledge/tree.md`, and `how/should/legacy/documents/be/ingested/into/a/knowledge/tree.md`.
