---
name: knowledgetrees-lookup
description: 'Use for new questions and failed probes: query kt first, read checked answers, determine whether missed leaves exist, and capture missing knowledge before continuing.'
metadata:
  scope: public knowledge-tree example
  source: "Owner explicit all-scales knowledge requirement; canonical procedure review, 2026-09-14"
  review_when: Recheck when retrieval gates, bootstrap, or knowledge-tree procedures change.
  status: unverified
---

For every new question, use `kt` before external search or host probes, unless the
answer is already present in adequately checked loaded knowledge. A known path
can be read directly with `kt open`; otherwise use a question-prefix call such
as `kt where is vivado` or `kt how to make a plan`. Use `kt find` when a broad
keyword search is intended. No need to reload the skill or orientation per query.

The kt-first rule applies at every scale, including code-comment-level questions:
what a function does and why, what a file contains, where a typedef lives, include
order, dependencies, invariants, and folder structure. Consult the owning tree
before source probes for a new implementation question. A missing fine-grained
answer creates the same investigation and capture obligation as a missing spec or
architecture answer; smallness and source visibility are not exemptions.

## Query, read, and resolve misses

1. State the question and use its prefix: `where is` -> `where/is/`,
   `how to` -> `how/to/`, `when to` -> `when/to/`, `what is` -> `what/is/`,
   `why does` or `why is` -> rationale. Full grammatical paths remain the convention.
   kt consumes matching directory words; at the first mismatch it searches only
   that branch using the remaining words. If best keyword coverage is below its
   threshold it climbs one parent and retries; it does not start with whole-tree search.
   An exact leaf hit returns the full leaf, not a ranked excerpt. `kt how to _`
   lists the prefix branch. Matching is lexical/content-based, not a semantic model;
   scores and widening thresholds are heuristics, not evidence of correctness.
   Empty or weak-only keyword results exit 1 while showing suggestions. The default
   minimum is 60% coverage of non-grammatical query terms (`--min-coverage` tunes it).
   Exit 0 means retrieval met a heuristic, not semantic adequacy or verification.
2. Read likely matches with `kt open local:PATH` or `kt open global:PATH`.
   Prefer project answers for project questions and global answers for host tooling.
   Results and orientation previews are not substitutes for the full answer.
3. Check `scope`, `source`, `verification`, `verified_at`, expiry metadata, and `review_when`.
   Freshness depends on volatility and evidence, not timestamp recency alone. Read
   the assertion and predicate behind every proof before relying on the claim.
   Run `kt prove --root ROOT TOKEN`. Green may be used. Yellow is a warning that
   prohibits relying on the contents until re-verification. Brown means the tree
   is busted; stop, diagnose the falsification or failed proof, and repair the leaf.
4. If `kt` does not find the information, you MUST determine whether a leaf exists.
   Retry distinctive keywords and synonyms, then try plausible sentence paths
   from known orientation routes with `kt open`. List only the nearest existing
   parent and descend or backtrack incrementally; a guessed path is not evidence.
   Start under `how/`, `what/`, `where/`, or `why/`; use `when/` when present.
   Only after this, use bounded listing/content search in the relevant branch. Recursive
   whole-tree/whole-repository enumeration is a last-resort diagnostic after
   semantic descent and bounded search fail, never the orientation mechanism.
5. Stop when a sufficiently checked answer and necessary qualifications are known.
   Then use the answer within current permissions and task scope.

Each directory choice narrows the question; context holds only the answer needed
now. A leaf may coexist with a same-stem directory of refinements. Narrower roots
refine broader knowledge but cannot weaken governing instructions. Do not inspect
unrelated projects merely because a search reveals them.

## Close the question before resuming work

An existing checked answer needs no duplicate leaf. A miss must be classified:
existing leaf (retrieve or rewrite it), or absent leaf (add it at the correct scope).
If no leaf exists, investigate safely, verify from primary evidence, and capture
the answer before the next unrelated tool call or completion. Necessary verification
and capture calls are allowed while resolving the question. Capture even small answers;
do not postpone them to a documentation phase or suppress them to keep leaf count low.
If unresolved, record `status: unresolved`, `checked_at`, the blocker, and next check
without inventing a verified conclusion. If writes are forbidden, give a scoped handoff.

Do not treat a zero-result query, an unreadable root, or a broken/missing `kt`
executable as evidence of absent knowledge. If `kt` is off PATH, use the installed
`~/.knowledge/.tools/kt`; report access/tool defects and use authorized semantic
retrieval rather than bypassing permissions.

Failed probes, installation/privilege steps, host changes, environment-specific
paths/tools/devices, and outside-repository writes are explicit reminders to apply
the same lookup rule, not exceptions or permission to improvise.

Knowledge of paths, privilege procedures, and policy does not authorize access,
installation, escalation, or other host changes. A permission denial is also a
retrieval event, not permission to bypass the boundary.

Root access policies govern widening. Read `how/to/control/knowledge/root/access.md`.
An access-required (exit 3) response is not a lookup miss or proof of absence.
Respect user-enabled bypass while retaining force-private exceptions. Do not
approve a root yourself, bypass the policy with direct reads, or treat stored
knowledge as consent. Ask the user to decide the scope; existing session/persistent
grants avoid repeated requests. Parent directories are not discovered automatically.
