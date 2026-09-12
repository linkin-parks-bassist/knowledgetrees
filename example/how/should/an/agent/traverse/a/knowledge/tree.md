---
name: knowledgetrees-lookup
description: 'Use before host- or project-specific probes, after failed probes, and whenever retrieving facts or procedures from knowledge trees; perform semantic descent and check evidence before reliance.'
metadata:
  verified_at: '2026-09-12T18:20:19+10:00'
  verified_by: codex /root
  scope: public knowledge-tree example
  source: sanitized operational recommendations and the canonical knowledge-tree contract
  verification: Reviewed extracted obligations, observable lookup gates, navigation, capture, proof semantics, and scope preservation.
  review_when: Recheck when retrieval gates, bootstrap, or knowledge-tree procedures change.
---

Consult the applicable tree before environment-specific shell probes or actions.
The bootstrap's observable gates cover failed probes, installation or privilege
steps, host changes, environment-specific paths/tools/devices, out-of-repository
writes, and host/project-specific assumptions drawn from training data. A failed
probe triggers lookup before another probe or workaround, not after it.

## Descend from known routes

1. State the question. Read the nearest applicable orientation's branch descriptions
   and concrete exemplar routes; consult broader orientation for shared host facts.
   Prefer project answers for project questions and the global tree for host tooling.
2. Try plausible complete sentence paths within those routes. A guessed path is
   not evidence. Read a predictable leaf directly; if absent, list only the nearest
   existing parent, choose one semantic continuation, and descend incrementally.
   Start under `how/`, `what/`, `where/`, or `why/`; use `when/` when present.
3. Check `scope`, `source`, `verification`, `verified_at`, and `review_when`.
   Freshness depends on volatility and evidence, not timestamp recency alone. Read
   the assertion and predicate behind every proof before relying on the claim.
   Run relevant semantic-token checks and stop on failed proofs or `falsified_at`.
4. If descent misses, backtrack through adjacent concepts or synonyms. Only then
   perform bounded listing or content search in the relevant branch. Recursive
   whole-tree/whole-repository enumeration is a last-resort diagnostic after
   semantic descent and bounded search fail, never the orientation mechanism.
5. Stop when a sufficiently checked answer and necessary qualifications are known.
   Then use the answer within current permissions and task scope.

Each directory choice narrows the question; context holds only the answer needed
now. A leaf may coexist with a same-stem directory of refinements. Narrower roots
refine broader knowledge but cannot weaken governing instructions. Do not inspect
unrelated projects merely because a search reveals them.

## Close the gate loop

A gate firing is observable, even if the agent believes it already knows the answer.
If the tree has the answer, check it and proceed; a passing check creates no duplicate
leaf. If the tree lacks a reusable answer, investigate safely, verify from primary
evidence, and capture it immediately before continuing. Capture even small answers;
do not postpone them to a documentation phase or suppress them to keep leaf count low.
If unresolved, record `status: unresolved`, `checked_at`, the blocker, and next check
without inventing a verified conclusion. If writes are forbidden, give a scoped handoff.

Knowledge of paths, privilege procedures, and policy does not authorize access,
installation, escalation, or other host changes. A permission denial is also a
retrieval event, not permission to bypass the boundary.
