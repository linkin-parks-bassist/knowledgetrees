---
verified_at: '2026-09-12T16:50:03+10:00'
verified_by: codex /root
scope: public knowledge-tree example
source: sanitized operational recommendations and the canonical knowledge-tree contract
verification: Reviewed extracted obligations, observable lookup gates, navigation, capture, proof semantics, and scope preservation.
review_when: Recheck when retrieval gates, bootstrap, or knowledge-tree procedures change.
---

Capture a reusable answer immediately after discovering and verifying it, before
using it to continue surrounding work. Observable lookup gates make misses explicit:
a checked tree hit needs no duplicate capture; a miss followed by discovery needs
an updated semantic owner or a new leaf. The agent's own uncertainty remains an
additional capture signal, not the only trigger.

## Choose the owner and path

Put host/personal tooling in `~/.knowledge` and project/subsystem facts in the
nearest applicable local root. Never promote professional, customer, partner, or
restricted material into the global tree; sanitize anything intended for publication.
Reread an existing owner before editing to preserve concurrent changes.

Write the full natural-language question first. Lowercase it, remove only punctuation
not belonging to a literal identifier, replace spaces with `/`, and add `.md` to
the last word. Keep grammatical words such as `to`, `is`, `the`, `of`, and `for`.
The slash-expanded path must read as the complete question. Hyphenate genuinely
multi-word components; never use underscores or implementation-shaped category
buckets. For example, "how to check knowledgetree proofs" becomes
`how/to/check/knowledgetree/proofs.md`.

Write the answer first, then the context, preconditions, limits, eligible proofs, and
links needed to use it. Leaves directly answer their paths rather than outsourcing
the answer to internal monolithic documents. Link alternate routes to a canonical
answer instead of copying it; record the conclusion and the distinction that made
it non-obvious, not chronology or stream of consciousness.

## Size and provenance

Semantic atomicity is guidance, not a word-count cap or automatic partitioning rule.
Consider relation, likely queries, joint use, ownership, lifecycle, volatility,
fan-out, retrieval cost, and drift. A cohesive answer may be substantial. Expect
many short leaves and fewer long ones, but never impose a distribution or file quota.
Splitting and consolidation both require judgment, not mechanical optimization.
Orientation and repository spine leaves deliberately aggregate coordinated truths;
do not thin them into catalogs or inflate them with unrelated archive material.

A verified leaf includes `verified_at` (ISO 8601 with timezone), `verified_by`, `scope`,
`source`, `verification`, and `review_when`. Put them under `metadata` when the leaf
also serves as `SKILL.md`. Name evidence actually checked and do not overstate it.
Whole-leaf `verified_at` requires independent review of everything in the leaf; proof
execution alone never earns it. An unresolved reusable question instead records
`status: unresolved`, `checked_at`, blocker, and next check.

## Narrowly eligible executable proofs

Add a proof for a single concrete true/false assertion whose truth a tiny local
read-only predicate can check immediately. Do not add proofs to commands,
requirements, policy, plans, history, opinions, bundled assertions, or non-trivial
conclusions. Split independent assertions only when that makes semantic sense;
otherwise use truthful provenance. The cadence is:

    The single mechanically verifiable assertion.

    Proof: (verified at _)

    ```bash
    the_read_only_predicate
    ```

The marker is a standalone paragraph between assertion and supported executable
fence. Bash, sh, Python, and Python3 are supported. An unmarked code block is an
instruction or example, not a proof. Predicates must be bounded, self-contained,
small enough to inspect at a glance, and return 0 exactly when the preceding
assertion is true. They must not write files, install, mutate services, launch
persistent processes, or have other externally visible side effects. Never use
`true` as a placeholder; prefer quiet `test` queries or a few direct assertions.

Inspect and run the predicate before relying on its assertion. An eligible
assertion without a marked proof, or a marker whose predicate is unsafe or tests
a different assertion, is a defect to repair within current authority before
reliance. A passing run
refreshes only its `Proof: (verified at …)` marker. A failing run changes it to
`Proof: (falsified at …)` and sets sticky leaf `falsified_at`. The verifier cannot
decide semantic eligibility, faithful coverage, or whether all prose is proved;
the agent remains responsible. Read maintenance before repairing a falsified leaf.
