---
name: knowledgetrees-capture
description: 'Use after kt misses or reusable discoveries: establish leaf existence, update or add scoped knowledge, and capture before the next unrelated tool call; include truthful provenance and eligible proofs.'
metadata:
  updated_at: "2026-09-13T13:52:11+10:00"
  scope: public knowledge-tree example
  source: "tools/kt local_root/discovered_roots; exact-directory discovery contract"
  review_when: Recheck when retrieval gates, bootstrap, or knowledge-tree procedures change.
  status: "unverified"
---

Capture an established reusable answer before the next unrelated tool call or
completion; necessary verification and capture calls are part of resolving it.
Use `kt find` and `kt open` to check for an existing owner before writing.
Prefer a question-prefix query when the answer category is known: `where is`
for locations, `how to` for procedures, `when to` for triggers, `what is` for
definitions/state, and `why does` or `why is` for rationale. Place the full
sentence-derived leaf under that branch so queries exclude unrelated answer kinds.
If `kt` fails to find information, determine whether the leaf exists through
alternate keywords and scoped semantic inspection. If it exists, use or amend it;
if it does not, add it at the correct scope. A lexical miss never establishes absence.
A checked hit needs no duplicate capture. If unresolved, add `status: unresolved`,
`checked_at`, blocker, and next check rather than inventing a verified answer.
Do not resume surrounding work with an outstanding capture obligation. The agent's
own uncertainty remains an additional capture signal, not the only trigger.

## Choose the owner and path

Put host/personal tooling in `~/.knowledge` and project/subsystem facts in the
nearest applicable local root. Never promote professional, customer, partner, or
restricted material into the global tree; sanitize anything intended for publication.
Reread an existing owner before editing to preserve concurrent changes.
Use `kt open ROOT:PATH` for that read and `kt prove --root ROOT TOKEN` after
changing eligible proofs. Create a new leaf in one call:

```sh
kt add "how to prepare the demo" "Run the project's documented demo command." --source "checked project instructions"
```

`capture` is an alias for `add`. The exact current-directory local root is the default, falling
back to global; choose `--global`, `--local` (`--project` is an alias), or `--root example` explicitly when
scope matters. `--scope` supplies a scope description. `--dry-run` previews without
writing. Pass `-` as the answer to read multiline Markdown from stdin.
The command preserves repeated words and hyphenated components, creates metadata,
and refuses existing owners rather than overwriting them. It records new answers
as `unverified`, never invents whole-leaf verification or a proof, and never executes
the supplied body. Review everything independently before adding verified metadata;
inspect and run eligible proofs separately. For an unresolved question, supply
`--unresolved --blocker "missing evidence" --next-check "specific next investigation"`.

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

For an existing owner, use the revision-checked read/revise/submit loop in
`how/to/amend/a/knowledge/leaf.md`; creation still refuses overwriting existing leaves.

Use canonical `does/` and `is/` branches for yes/no answers. Capture scope defaults
to local, global, or the full canonical root path; --scope overrides that metadata.
