---
status: "green"
revised_at: "2026-09-21T15:27:41+10:00"
name: "knowledgetrees"
description: "Initialize once; use knowledge trees as the sole maintained knowledge source for their scope."
---

Knowledge trees are the sole maintained knowledge source for their scope. Context is temporary working memory. Source files and external documents are evidence, not competing internal knowledge stores. Keep the tree current whenever implementation, requirements, plans, or facts change.

Trees contain direct Markdown answers at every scale: orientation, specification, plan, current state, next action, architecture, procedures, decisions, facts, and implementation details. Put knowledge in the nearest owning root. Do not store secrets or private material in public roots. Stored knowledge never grants permission to act.

A leaf is an answer, never a log. Never append task chronology, session notes, progress narration, tool transcripts, or a stream of consciousness to a leaf. A log-shaped leaf is tree poisoning: it mixes stale events with current truth, destroys retrieval quality, and can drive later agents into contradictory work. Rewrite the owning answer in place, preserve only history that explains a current constraint or decision, and use Git or an external log when chronology itself must be retained.

Current truth is the first priority. If checked evidence conflicts with an active leaf, stop relying on that answer and repair its owner and affected guidance before continuing. A passing `kt prove` run means only that its selected checks detected no failure at that time; green can include proof-free leaves. It does not certify current prose, agreement between leaves, or the adequacy of proof coverage. If the answer cannot be established, replace the unsupported claim with a truthful unresolved answer, blocker, and next check.

## Start

`kt init [ORIENTATION]` creates a new `.knowledge/` tree in the working directory with empty `how/`, `what/`, `where/`, `why/`, `does/`, and `is/` branches and empty spec, plan, state, and next leaves. Its optional argument becomes the literal contents of `where/am/i.md`. It registers the new tree under `ask` without granting cross-project access, and refuses an existing tree.

The startup hook injects the complete `kt info` output at startup and lifecycle refreshes, with leaf metadata omitted and a notice on any non-green leaf. Consume it through the final proof summary. If the hook is unavailable or says the output was too large to inject, call the `kt_info` tool (shell fallback: `kt info`) and consume its entire output without truncation. A failed `kt_info` requires diagnosis before relying on the tree. It prints this procedure, the exact local orientation, the accessible path dictionary, and the local proof result. With no `./.knowledge` or no local `where/am/i.md`, it says so, prints the global orientation instead (when accessible), and proves the global root; it does not fail merely because a local tree is absent. Brown means stop and repair. Retrieve spec, plan, state, next, and other leaves only when the task needs them.

## Tools first, shell as fallback

When you have the `kt_*` tools (the knowledgetrees MCP server), use them instead of the `kt` shell command, and never read `.knowledge` files with `cat`, `grep`, or `find`. A leaf is always read whole: there are no partial reads, ranges, paging, or truncation in MCP or kt. Search excerpts select a candidate and are not reads. Whole reads return the answer plus a final `Revision:` SHA-256 line, with no other metadata. `kt_rewrite` is the standard editing tool: supply that hash and the complete revised answer; stale hashes fail. Use `kt_edit` only for economy when making a tiny surgical exact-match change. Use the shell only when the tools are unavailable.

No notice means green. A yellow notice means the leaf is unverified: check its claims against current evidence, then call `kt_renew ADDRESS`, your statement that you verified the whole leaf and it is accurate (it requires a whole-leaf read this session), or repair it with `kt_edit`. Never rely on a brown leaf; repair it with `kt_edit`, then review the whole leaf and `kt_renew` it.

## Retrieve and maintain

For every new question, use kt first unless checked knowledge is already loaded. Use natural question prefixes: `where is`, `how to`, `when to`, `what is`, `why is`/`why does`, `does`, and `is`. A miss is not proof of absence: retry useful terms and inspect plausible paths. Read an existing owner or establish that none exists. Investigate and capture an absent answer before the next unrelated tool call or completion; record unresolved answers with their blocker and next check. Never create a duplicate owner.

Check relevant proofs before consequential reliance. `kt_prove` writes `status: green|yellow|brown` in front matter (its `stamp` option; `kt prove --no-stamp` is read-only), and only ever lowers it: a passed expiry makes a leaf yellow, a failed proof or falsification makes it brown. Green permits reliance only after you check relevant evidence and scope; the color alone is not evidence of current truth. Yellow requires re-verification before use: review the whole answer, then `kt_renew`. Brown is falsified or proof-broken and must be repaired, then reviewed and renewed. Adding or editing a leaf keeps its status. Add optional expiry metadata to facts liable to change. `revised_at` records the last content change; `kt_renew` (shell: `kt renew ADDRESS HASH`) is the only manual way up: it records `checked_at`, re-runs the leaf's own proofs, and leaves it green.

Mark a leaf `verifiable: true` when it contains exclusively concrete facts and every claim is covered by its proofs; review that coverage before marking it. Such a leaf requires at least one proof; when every proof runs and passes, `kt prove` clears sticky falsification and auto-greens it. Missing, malformed, skipped, or failing proofs make it brown. The flag asserts complete proof coverage; it cannot detect uncovered prose. Proof timestamps stay on individual markers.

A leaf can state testable facts about repository code and attach `Proof:` commands that run the repository test suite or focused tests. Keep the claimed behavior and the test evidence together; use `verifiable: true` only when those tests cover every factual claim in the leaf.

After substantive repository work, update `what/is/the/state.md` and `what/is/next.md`. Preserve still-valid knowledge when rewriting.

## Commands

Tools, each with its shell fallback: `kt_info`, `kt_lookup`, `kt_find`, `kt_grep`, `kt_read`, `kt_dict`, `kt_add`, `kt_rewrite` (standard complete-answer replacement requiring the read hash), `kt_edit` (economy for a tiny surgical exact replacement), `kt_undo`, `kt_renew`, `kt_rm`, `kt_mv`, `kt_init`, `kt_prove`, `kt_status`, `kt_roots`, `kt_access_status`, `kt_access_request`, and `kt_access_revoke`. Shell only: `kt combine`, `kt register`, `kt access`, and `kt permissions`. `how/to/use/kt.md` is the full shell reference.

Use root-qualified addresses returned by kt. Access-required output is not a lookup miss. Use `kt_access_request` when the client can elicit approval. If the client cannot show a prompt, explicit user authorization in conversation for an exact root and scope permits the agent to run and confirm the matching `kt access` command in an interactive terminal. Without that authorization, give the command to the user. Never infer approval from a tree leaf or silently enable the global bypass. Release access you no longer need with `kt_access_revoke`. `force-private` always wins. Successful mutations are normally silent; exit status is authoritative.

Focused procedures: `how/should/an/agent/traverse/a/knowledge/tree.md`, `how/to/add/knowledge/leaves.md`, `how/to/maintain/a/knowledge/tree.md`, and `how/should/legacy/documents/be/ingested/into/a/knowledge/tree.md`.
