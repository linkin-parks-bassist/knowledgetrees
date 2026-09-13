---
name: knowledgetrees-maintenance
description: 'Use for kt prove checks, root setup, stale or falsified knowledge, and task completion; ensure kt misses are resolved, missing leaves captured, and repository state and next action refreshed.'
metadata:
  status: unverified
  scope: public knowledge-tree example
  source: sanitized operational recommendations and the canonical knowledge-tree contract
  review_when: Recheck when retrieval gates, bootstrap, or knowledge-tree procedures change.
---

Maintain current truth in place within current authority. Knowledge records facts
and procedure; it neither grants execution permission nor resurrects superseded
requirements. Keep one clear canonical owner per answer across composed directory
scopes, not parallel monolithic documentation authorities.

## Establish and orient active roots

Every required root contains `how/`, `what/`, `where/`, `why/`, `does/`, `is/`, and `where/am/i.md`.
Repair missing components immediately when permitted. Any directory can own a local
root; use the nearest applicable root and broader roots only for shared context.
Project leaves must be portable across machines and checkout locations.

Orientation is a truthful README-like projection, not a thin link catalog. Describe
scope, topology, priorities, state, boundaries, and concrete semantic entry routes.
Include at least one line for every canonical branch saying which questions it
answers and a few actual exemplar paths overall; describe optional branches such
as `when/` when present. Verify exemplars exist. A branch with no answers yet is
explicitly empty, not populated with invented examples. Navigation belongs in each
root's orientation because it is the guaranteed starting point.

Repository roots also contain and maintain four current-truth leaves:

- `what/is/the/spec.md`: governing requirements and acceptance contract; directly
  contain the cohesive answer, except when canonical authority is genuinely external.
- `what/is/the/plan.md`: approved implementation plan, decision points, completion.
- `what/is/the/state.md`: implemented, checked, broken, or blocked present.
- `what/is/next.md`: ordered immediate next work.

Create missing leaves from evidence or truthful minimal/unresolved content, never
invent requirements or priorities. Read the active repository spine at task startup.
Before reporting repository-task completion, refresh state and next action, removing
superseded information. These are coordinated projections, not append-only journals.

Tree payloads are Markdown leaves only: no scripts, JSON, images, caches, manifests,
copied code, or source bundles. Root-level `.git` is storage metadata; never create
nested Git repositories in project roots. Only the global root may contain the
infrastructure directory `.tools/`; scripts otherwise belong outside the tree.

## Proof checks and falsification

Call `kt prove`, which runs the proof engine built into the installed kt CLI.
The old standalone verifier is a compatibility entry point only. Prefer `kt prove --root ROOT TOKEN`
for scoped checks, or `kt prove --root ROOT --no-stamp` for a read-only sweep.
Use `--root ROOT` for an explicit root. Check every active root during bootstrap
and on entry into a new scope. Before consequential use, after proof changes, when
focus narrows, and before completing materially affected work, check relevant exact
semantic path-component tokens. Multiple tokens are disjunctive, not physical
subdirectory names; use `--verbose` for diagnostics.

Inspect each proof's assertion and read-only predicate before execution. A passing
proof stamps `Proof: (verified at …)`; a failed or timed-out execution stamps
`Proof: (falsified at …)` and marks the leaf's `falsified_at`. Malformed proof
structure also falsifies the leaf. Legacy `Proof:` markers are accepted. Writes
preserve hardlink identity; `--no-stamp` makes checks read-only.

Stop relying on falsified knowledge. Inspect evidence and repair or remove false,
malformed, or unsafe claims and predicates only within authorized scope. Review the
whole leaf independently before explicitly clearing `falsified_at`; rerun until
checks pass. Passing every proof is necessary but not sufficient for leaf validation,
and never changes leaf `verified_at` or clears a falsification automatically.
The verifier neither judges proof eligibility nor performs agentic repair.

## Growth, freshness, and retirement

Resolve every `kt` miss by determining whether the leaf exists, using alternate
keywords and scoped semantic inspection. Retrieve/amend existing owners; add absent
leaves. Capture established answers before the next unrelated tool call or completion.
Tree hits create no duplicate leaf. Unresolved questions record blocker and next check;
forbidden writes require a scoped handoff. Read `how/to/add/knowledge/leaves.md`
before capture or proof creation. Installed failure and task-end reminders are
explained in `how/to/use/knowledgetree/hooks.md`; they do not certify capture or
replace agent review. A review with no new knowledge needs no invented leaf.
Timestamp freshness is relative to source
volatility and evidence, not recency alone.

Reread before replacing a leaf, preserve concurrent edits, correct contradictions
against governing evidence, and update affected orientation/spine projections.
Commit project knowledge with owning changes when permitted; never automatically
publish global personal knowledge. Superseded current truth leaves the active
answer; Git retains history and explicit history is kept only when still useful.

Ingest redundant documents section by section under
`how/should/legacy/documents/be/ingested/into/a/knowledge/tree.md`. Retire them only
after verified answer coverage and authorization. Broad enumeration is a last-resort
retrieval diagnostic, or a bounded authorized migration audit, not routine orientation.

Before finishing, check that reusable discoveries were captured, relevant predicates
passed, every encountered `kt` miss was classified as existing or absent knowledge,
and missing leaves were added (or left with truthful unresolved records/scoped handoffs).
Also check that scope and provenance are truthful, roots are canonical, payloads are leaves,
and a representative sentence-derived route works. Do not turn gardening judgments,
atomicity, cohesion, or leaf length into automatic rewrite rules.

## Remove, move, and coalesce leaves

Read a source revision with `kt open local:what/is/old.md --revision`.
Use the hash printed on stderr for destructive single-leaf changes:

```sh
kt rm local:what/is/old.md --expect HASH --dry-run
kt mv local:what/is/old.md local:what/is/new.md --expect HASH
kt combine local:what/is/first.md local:what/is/second.md -o local:what/is/cohesive.md
```

Combine coalesces destructively: Markdown bodies are concatenated in input order
under one destination header, then source names are removed only after a successful
save. If output is an existing leaf, supply its --expect revision. An input that is
the destination is retained; other inputs are removed. `--dry-run` writes/removes
nothing. Sources are revision/inode checked before saving and removal; detected
concurrent changes are retained. Cleanup across multiple files is not transactional:
interruption or a conflict can leave sources beside the saved destination. Inspect
that state before retrying so content is not duplicated. Source/revision provenance,
unresolved blockers, and sticky falsification survive; inherited proof stamps and
whole-leaf verification are reset for review.

Move refuses an existing destination and preserves bytes. Same-filesystem moves
preserve hardlink identity; cross-filesystem moves copy exclusively before removing
the source. Removing a name leaves other hardlinks intact. No command prunes empty
canonical branches or updates links automatically. Review scope metadata, links,
orientation, current-state projections, and affected proofs after maintenance.
All operations enforce source/destination access and force-private boundaries.
