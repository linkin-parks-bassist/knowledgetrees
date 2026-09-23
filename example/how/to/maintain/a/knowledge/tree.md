---
status: green
revised_at: "2026-09-24T08:08:12+10:00"
name: "knowledgetrees-maintenance"
description: "Use for kt prove checks, root setup, stale or falsified knowledge, and task completion; ensure kt misses are resolved, missing leaves captured, and repository state and next action refreshed."
---

Maintain current truth in place within current authority. Knowledge records facts
and procedure; it neither grants execution permission nor resurrects superseded
requirements. Keep one clear canonical owner per answer across composed directory
scopes, not parallel monolithic documentation authorities.

## Current truth first

Treat known stale, poisoned, or contradictory active knowledge as an immediate
repair task, even when its metadata says green or its proofs pass. Stop relying
on the affected answer. Check current source evidence, read the full owning leaf,
and rewrite it before unrelated work; preserve its still-valid claims. Correct
other active leaves and guidance that repeat the same error. If evidence cannot
settle the answer, remove the unsupported claim and record the blocker and next
check in a truthful unresolved answer. Surface any remaining unsafe reliance.
A passing `kt prove` run means only that the selected checks found no detectable
failure at that time. Green includes proof-free leaves and does not certify current
prose, consistency between leaves, or proof coverage. Even `verifiable: true`
relies on an author-reviewed coverage assertion and faithful predicates.

After a behavior or policy change, build an explicit affected-owner inventory before editing: narrow implementation leaves, broader procedures and policy, the central `how/to/use/knowledgetrees.md`, repository spec/plan/state/next, orientation when its routes changed, public example, README and CLI help, startup payloads, generated copies, and installed guidance. Search both directions: use `kt_grep` and repository search for distinctive old claims, counts, tool lists, fallbacks, and limitations, and also search for the new behavior to find partial presentations. Read every relevant hit in context and compare meaning, not just matching strings. Repair all owners, refresh generated and installed guidance, then repeat the negative searches. Run tests, proofs, and instruction-sync only after that semantic pass. Do not report a change as destaled or complete while any affected owner is unchecked, contradictory, or still describes superseded behavior. This is an affected-scope change gate, not a startup inventory of unrelated roots.

## Establish and orient active roots

Every required root contains `how/`, `what/`, `where/`, `why/`, `does/`, `is/`, and `where/am/i.md`.
Repair missing components immediately when permitted. Any directory can own a local
root; kt discovers the exact current-directory tree and explicitly registered
roots, not parents. Use broader roots only within their access policy.
Project leaves must be portable across machines and checkout locations.

Orientation is a truthful README-like projection, not a thin link catalog: it
explains the repository, its contents, and an overview of what is in the tree.
Describe scope, topology, priorities, state, boundaries, and concrete semantic
entry routes. Include at least one line for every canonical branch saying which
questions it answers and a few actual exemplar paths overall; describe optional
branches such as `when/` when present. Verify exemplars exist. A branch with no
answers yet is explicitly empty, not populated with invented examples. Orientation
contains no general knowledge-tree usage instructions (query conventions,
traversal strategy, how to use `kt`): those are owned by the bootstrap procedure
and hooks, not by the orientation leaf.

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
A leaf is a current answer, never a log. Appending chronology, session notes, progress
narration, tool transcripts, or stream of consciousness is tree poisoning: it mixes
stale events into current truth and makes retrieval mislead later agents. Rewrite the
answer in place. Keep history only when it explains a present constraint or decision;
use Git or an external log when chronology itself matters.
These two deranging failure modes—active inconsistency and logleaves—are defined
at `what/is/tree/poisoning.md` and must be avoided at all costs.

Tree payloads are Markdown leaves only: no scripts, JSON, images, caches, manifests,
copied code, or source bundles. Root-level `.git` is storage metadata; never create
nested Git repositories in project roots. Only the global root may contain the
infrastructure directory `.tools/`; scripts otherwise belong outside the tree.

## Proof checks and falsification

Call `kt_prove` (shell fallback: `kt prove`), which runs the proof engine built into the installed kt CLI. Prefer its `root` argument and exact path-component tokens for scoped checks; omit `stamp` for a read-only sweep.
Use `--root ROOT` for an explicit root. ROOT is the exact allowed knowledge-tree directory shown by `kt roots` (normally PROJECT/.knowledge), not the containing repository directory. If a mistaken repository path returns access-required, correct it to the already allowed tree root; do not grant access to a new root merely to repair that argument. Check the current local root during bootstrap
and on entry into a new project scope. Do not enumerate or sweep every accessible
root at startup; broader answers are checked when needed. Supplied orientation
content need not be reread. Before consequential use, after proof changes, when
focus narrows, and before completing materially affected work, check relevant exact
semantic path-component tokens. Multiple tokens are disjunctive, not physical
subdirectory names; use `--verbose` for diagnostics.

Inspect each proof's assertion and read-only predicate before execution. A passing
proof stamps `Proof: (verified at …)`; a failed or timed-out execution stamps
`Proof: (falsified at …)` and marks the leaf brown. Malformed proof
structure also makes the leaf brown. Writes
preserve hardlink identity; `--no-stamp` makes checks read-only.

`kt prove` always reports green, yellow, and brown totals and prints brown
root-qualified leaf paths. Leaves are green by default, including non-verifiable
specifications, plans, procedures, and opinions, and adding or editing a leaf keeps
its status. Proof evaluation only lowers a status: elapsed expiry makes a leaf yellow
pending manual review, and it stays yellow until `kt_renew`, except when all declared
proofs pass on a `verifiable: true` leaf. The coverage
claim and predicates still require agent judgment. Do not rely on a
currently yellow leaf until re-verification.
Brown is falsified, malformed, or proof-failing and makes `kt prove` fail because
the tree is busted.
Normal evaluation persists `status: green|yellow|brown` in front matter.
`kt_renew` (shell: `kt renew ADDRESS HASH`) records `checked_at` only after manual review and re-evaluates the leaf.
`--no-stamp` is read-only. Content rewrites refresh `revised_at` and keep the
status. Manual review (`kt_renew`) is needed to renew expiry, clear a yellow mark,
or clear unflagged sticky brown status.

Stop relying on falsified knowledge. An agent encountering a brown leaf must inspect
evidence and repair or remove false,
malformed, or unsafe claims and predicates only within authorized scope. Review the
whole leaf independently and use `kt_renew` to clear brown status; rerun until
checks pass. Passing every proof is necessary but not sufficient for an unflagged
leaf. A reviewed `verifiable: true` leaf is the narrow exception: complete passing
proofs clear falsification automatically. The verifier
cannot judge whether the flag's complete-coverage assertion is truthful and does
not perform agentic repair.

## Maintain knowledge at every scale

Keep function contracts and rationale, code-comment-level details, file contents,
typedef locations, include order, dependencies and repository structure current
alongside architecture and specs. Never prune a useful direct answer merely because
it is fine-grained or derivable from source. When implementation changes, review
its affected small leaves as well as broad state/spec projections, correcting stale
answers against current source evidence at the owning scope.

## Growth, freshness, and retirement

Resolve every `kt` miss by determining whether the leaf exists, using alternate
keywords and scoped semantic inspection. Retrieve/rewrite existing owners; add absent
leaves. Capture established answers before the next unrelated tool call or completion.
Tree hits create no duplicate leaf. Unresolved questions record blocker and next check;
forbidden writes require a scoped handoff. Read `how/to/add/knowledge/leaves.md`
before capture or proof creation. Startup-hook behavior is explained in
`how/to/use/knowledgetree/hooks.md`; non-startup reminder hooks are disabled and
agent review remains explicit. A review with no new knowledge needs no invented leaf.
Timestamp freshness is relative to source
volatility and evidence, not recency alone.
Leaves may declare an ISO-8601 `expires_at` or an `expires_every` duration measured
from manual `checked_at`. Elapsed expiry makes them yellow until independently re-verified.
Agents should add expiry metadata when a factual answer is liable to change. Do not
add expiry merely because content cannot be mechanically or independently verified.

Have the original contents in context before editing a leaf. Full reads are always
complete and return the revision hash; partial reads do not exist. Use `kt_rewrite`
as the standard method with that hash. Use `kt_edit` only for economy on a tiny
surgical exact change, or
in the shell use kt rewrite ADDRESS HASH BODY. Supply the answer body only. Use `--expires-at`, `--expires-every`, or `--verifiable` to set
optional metadata; `--no-expiry` or `--no-verifiable` to clear it. The required
hash rejects changed contents; reread and merge on conflict. Preserve still-valid
knowledge and concurrent edits, correct contradictions
against governing evidence, and update affected orientation/spine projections.
Commit project knowledge with owning changes when permitted; never automatically
publish global personal knowledge. Superseded current truth leaves the active
answer; Git retains history and explicit history is kept only when still useful.

Ingest redundant documents section by section under
`how/should/legacy/documents/be/ingested/into/a/knowledge/tree.md`. Retire them only
after verified answer coverage and authorization. Broad enumeration is a last-resort
retrieval diagnostic, or a bounded authorized migration audit, not routine orientation.

Before finishing, complete the current-truth consistency gate for affected behavior and guidance. Account for every item in the affected-owner inventory and retain the negative-search terms used to look for superseded claims until those searches return no unexplained hits. Check that the central procedure and focused procedure owners were updated whenever their workflow changed, reusable discoveries were captured, relevant predicates passed, every encountered `kt` miss was classified, and absent answers were added or truthfully left unresolved. Also check that scope and provenance are truthful, roots are canonical, payloads are leaves, installed copies match their sources, and a representative sentence-derived route works. A test pass, green proof count, recent timestamp, or zero byte drift cannot by itself establish semantic freshness. Do not turn gardening judgments, atomicity, cohesion, or leaf length into automatic rewrite rules.

## Remove, move, and coalesce leaves

Read each source with `kt_read`. Use `kt_rm` and `kt_mv` with the returned Revision hash. Use `kt_combine` with an ordered address/revision object for every source and a destination revision when replacing an existing destination; it detects aliases of the same source. The shell commands remain fallbacks:

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
that state before retrying so content is not duplicated. Source bodies, including their blockers and next checks, are preserved. A brown
source keeps the destination brown; inherited proof stamps and manual check time
are reset for review.

Move refuses an existing destination and preserves bytes. Same-filesystem moves
preserve hardlink identity; cross-filesystem moves copy exclusively before removing
the source. Removing a name leaves other hardlinks intact. No command prunes empty
canonical branches or updates links automatically. Review leaf paths, links,
orientation, current-state projections, and affected proofs after maintenance.
All operations enforce source/destination access and force-private boundaries.
