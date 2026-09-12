---
name: knowledgetrees
description: 'Mandatory unified knowledge-tree procedure: establish canonical
  roots, orient and retrieve semantically, run leaf proofs, and immediately preserve
  every plausibly reusable answer discovered during work.'
metadata:
  verified_at: '2026-09-12T15:33:08+10:00'
  verified_by: codex /root
  scope: public knowledge-tree example and distributable skill
  source: sanitized adaptation of the canonical knowledgetrees procedure
  verification: Unified the former using and maintaining procedures; incorporated
    mandatory canonical-root and repository-spine repair, continuous atomic growth,
    narrowly eligible and explicitly labelled executable proofs, task-completion
    state updates, the tree-as-substrate model, incremental traversal, monolith
    ingestion, a bias rather than hard invariant toward semantic atomicity,
    deliberately aggregating orientation and spine projections, heavy-tailed leaf
    sizing, and hyphenated semantic components distinct from code-only snake_case;
    checked the independent verifier and the installer's hard-linked compatibility
    bootstrap behavior in an isolated target home; replaced per-task reinvocation
    with session-boundary bootstrap semantics.
  review_when: Recheck when the knowledge-tree design, scope rules, or agent harness changes.
---

Knowledge trees are federated semantic filesystem indexes. Directory choices narrow
a question and Markdown leaves answer it. Context is working memory, not storage:
retrieve only what is needed, and continuously preserve reusable discoveries in the
tree instead of expecting a later agent to repeat the work.

## Foundational model

The knowledge tree is the authoritative knowledge substrate and the agent-facing
retrieval interface. It is not a table of contents, catalog, link farm, or thin
navigation layer over human-oriented documentation. A leaf directly answers the
question expressed by its path; it must not merely send the reader to a monolithic
document for the answer. Semantic atomicity does not impose a small word count: a
cohesive answer may be substantial when its parts are normally needed together.

Design the knowledge for cheap agent retrieval. Traverse one semantic choice at a
time as uncertainty reveals itself, read the smallest answer that resolves that
uncertainty, and stop. Do not begin by enumerating the whole filesystem or knowledge
tree with recursive listings, broad `find`, broad `rg --files`, or equivalent
inventory operations. Those are last-resort diagnostics after semantic descent and
bounded branch search fail, not an orientation mechanism.

Human-oriented documents and task-specific instruction bundles are not parallel
knowledge authorities. When their content is in scope for a knowledge tree, treat
them as temporary ingestion sources: decompose their reusable facts into focused
semantic leaves, verify coverage, then retire the redundant source when authorized.
The installed `SKILL.md` is a compatibility bootstrap into this tree, not a pattern
for proliferating separate skill documents.

The hard operating obligations are:

- The tree contains the answers; it does not outsource them to internal documents.
- Leaf paths are semantic questions or concepts an uncertain agent can traverse;
  genuinely multi-word path components are hyphenated and never use underscores.
- Retrieval descends incrementally and stops when uncertainty is resolved.
- Every resolved reusable uncertainty is captured immediately.
- Legacy corpora are decomposed, coverage-checked, and retired rather than mirrored.
- Project leaves remain portable across machines and checkout locations.
- Delegated knowledge work is divided into tiny, reviewable crumbs; the integrator
  retains semantic coherence and deprecation decisions.

Leaf boundaries and other on-the-ground organization choices are not governed by
hard partitioning rules. They require contextual judgment by a reasoning agent. Use
the following as guidance, not invariants or automatic rewrite triggers:

- Tend toward independently retrievable semantic answers when that helps discovery.
- Expect that many leaves will be short and some cohesive leaves substantial, but do
  not target a distribution or file count mechanically.
- Consider splitting or combining knowledge from its degree of relation, likely
  discovery path, expected joint use, ownership, volatility, retrieval cost, and
  local context.
- Preserve a useful arrangement when the contextual case for changing it is weak;
  neither atomicity nor consolidation is an end in itself.

## Bootstrap and orientation

Invoke this skill once as the first bootstrap action of a fresh agent session,
before substantive task reasoning, discovery, planning, or other tool use. After it
is loaded, apply the procedure throughout that session without reinvoking it for
each user message, turn, or task. Rebootstrap only when a new session begins or a
context reset has genuinely lost the procedure. Entering a different project scope
within an already bootstrapped session requires orientation and proof verification
for the new scope, not another skill invocation.

For the active task scope, identify the nearest applicable project knowledge root
and the global `~/.knowledge` root. Do not inspect or modify unrelated projects just
because a search reveals them. Current instructions, permissions, and explicit
no-touch boundaries still govern.

Every required knowledge root must immediately contain the canonical directories
`how/`, `what/`, `where/`, and `why/`, plus `where/am/i.md`. If the active task's
project root or any canonical component is absent, create it before continuing.
Write a truthful, useful `where/am/i.md` from primary evidence; never invent an
orientation. It is a deliberately aggregating README-equivalent and may be sizeable:
include enough scope, topology, current priorities, important state, boundaries, and
semantic entry routes to orient an agent without broad discovery. If writes are
forbidden, report the exact defect rather than silently accepting it.

The semantic tree contains directories and Markdown knowledge leaves only. Every
payload file below a knowledge root must be a `.md` leaf; do not put scripts, JSON,
images, copied source trees, caches, manifests, or other implementation artifacts
inside it. Root-level version-control metadata such as `.git` is storage machinery,
not tree payload. The global root alone may also contain a root-level `.tools/`
directory for knowledge-tree infrastructure; it is not a semantic branch and must
never exist in project trees. Proof scripts themselves remain tiny inline blocks
inside leaves.

After establishing the active scope, run a whole-root proof check. Without a root
argument, the verifier treats the working directory itself as the root when it is
`.knowledge`; otherwise it uses `.knowledge` directly inside the working directory.
It checks all of that root when given no semantic tokens.

```bash
~/.knowledge/.tools/verify-knowledgetree-proofs
```

Do not continue with stale proof-backed knowledge when this check fails. Inspect
each reported assertion and evidence, repair or remove false claims and malformed
proofs immediately, then rerun until it passes. A passing run means every currently
marked proof in that root passed at that time; it does not validate unproved prose.

Read the nearest applicable `where/am/i.md` first and the global one as well. The
orientation leaf is the guaranteed README-like entry point for its scope. More local
knowledge may refine broader knowledge, but cannot silently weaken governing
instructions.

Every repository knowledge root must also contain these canonical current-truth
leaves:

- `what/is/the/spec.md`: the repository's cohesive governing requirements and
  acceptance contract. It may be a substantial long-tail leaf when that best answers
  “what is the spec?” Link to an external canonical owner only when authority
  genuinely lives outside the repository; never replace the answer with a pointer to
  an internal monolithic specification.
- `what/is/the/plan.md`: the current approved implementation plan, decision points,
  and completion criteria.
- `what/is/the/state.md`: what is currently implemented, verified, broken, or
  blocked.
- `what/is/next.md`: the ordered, immediately actionable next work.

Create any missing leaf immediately. Use truthful minimal content or an explicit
unresolved status when evidence is unavailable; never manufacture a spec, plan,
state, or priority. At task startup, read these four leaves when working in a
repository. Whenever an agent completes a repository task, it must update
`what/is/the/state.md` and `what/is/next.md` before reporting completion, removing
superseded state and recording the new verified present and next action. These are
maintained projections of current truth, not append-only task journals.

## Retrieval

Whenever a fact, procedure, environment detail, project rule, tool behavior, or
other needed answer is not immediately available, consult the knowledge trees before
researching elsewhere:

1. State the question and try a few plausible semantic paths. A guessed path is not
   evidence.
2. Read a likely leaf directly. If it is absent, list only the nearest existing
   parent, select the most natural semantic continuation, and descend. Start an
   unknown question under `how/`, `what/`, `where/`, or `why/`. A leaf may coexist
   with a same-stem directory of refinements.
3. Inspect `verified_at`, `source`, `verification`, `scope`, and `review_when`.
   Freshness is relative to volatility and evidence, not merely timestamp recency.
4. If descent fails, backtrack through adjacent concepts or synonyms. Only then list
   or search the nearest relevant branch, one level or bounded subtree at a time,
   followed by targeted content search. Recursive whole-tree or whole-repository
   enumeration is a last-resort diagnostic, never a first move.
5. Stop loading context when the answer and its necessary qualifications are known.

At important junctions, rerun the verifier against the relevant semantic path
tokens: when focus narrows to a subsystem or technology, before a consequential
decision relies on its facts, after changing proofs, and before completion when the
branch materially affected the result. Tokens match exact components anywhere in a
leaf's relative semantic path, rather than physical subdirectory roots. Multiple
tokens are disjunctive: a leaf is selected when any token matches. For example, from
the active repository this checks every proof in every leaf whose path contains the
`vivado` component:

```bash
~/.knowledge/.tools/verify-knowledgetree-proofs vivado
```

Invoke the verifier from the knowledge root or its containing directory. Otherwise,
select the intended root explicitly with optional `-r PATH` or `--root PATH`; all
positional arguments remain disjunctive exact semantic component tokens.

## Executable leaf proofs

Proof eligibility is deliberately narrow. Add a proof only when a knowledge leaf
contains a single, concrete true/false assertion whose truth can be checked
immediately and mechanically by a tiny local predicate. Do not add proofs to
instructions, command examples, opinions, policy or specification items, plan
items, historical explanations, non-immediate claims, compound assertions, or
non-trivial conclusions. If a sentence bundles several independently useful simple
facts, split it into atomic assertions and give each eligible assertion its own
proof. Otherwise rely on truthful provenance and verification metadata.

The cadence for an eligible assertion, with a separate proof-verification stamp, is:

    The single mechanically verifiable assertion.

    Proof: (verified at _)

    ```bash
    the_read_only_predicate
    ```

`Proof: (verified at _)` must appear as a standalone paragraph between the assertion
and its fenced Bash, Python, or similarly ubiquitous script. The verifier replaces
`_` with an ISO 8601 timestamp with timezone after that proof passes and refreshes
it on subsequent passing runs. Legacy bare `Proof:` markers remain accepted and are
upgraded on success. An executable block without
that marker is an instruction or example, not a leaf proof. The proof script must be
read-only, bounded, self-contained, small enough to understand at a glance, and
return status 0 if and only if the one immediately preceding assertion is currently
true. It must not write files, install anything, mutate services, launch persistent
processes, or perform any other externally visible change. Never use a placeholder
such as `true`. Prefer a direct `test`, a quiet command query, or a few Python
assertions; avoid output on success and remove caller-state ambiguity.

The reader must inspect and run every `Proof:` script before relying on its
assertion. An eligible assertion with no marker and proof is a tree defect: establish
the predicate and add both immediately. A marker without a safe eligible script, or
a script testing more than the immediately preceding atomic assertion, is also a
defect. If the script returns 0, the verifier refreshes only that proof's marker.
Leaf-level `verified_at` remains unchanged: it records an independent review of the
whole leaf, including statements not covered by proofs. Mechanical proof execution
does not establish whole-leaf verification. A failed proof receives
`Proof: (falsified at …)` and sets leaf-level `falsified_at` metadata. This flag is
sticky: later passing proofs do not validate the leaf or clear it. Checks continue
to fail until an agent independently reviews and repairs the leaf and explicitly
clears the flag. Passing all proofs is necessary but not sufficient for validation.
The verifier performs no agentic repair. Use `--no-stamp` for read-only checking.
If it is malformed, unsafe, or returns nonzero, establish current truth from primary
evidence and revise or remove the assertion, proof, and metadata immediately.

The global verifier validates marker structure and runs selected proofs, but it
cannot decide whether prose is proof-eligible or whether a predicate faithfully
tests one atomic assertion. The agent remains responsible for those semantic
judgments.

Current agent harnesses still require a skill-shaped bootstrap. Installers should
create each required `SKILL.md` as a hard link to the installed canonical leaf at
`~/.knowledge/how/to/use/knowledgetrees.md`; they must not create a separately
maintained skill body.

## Immediate growth and maintenance

Use the agent's own uncertainty as a mandatory capture signal. Any time an answer
was not immediately available and it is plausible that a future agent will ask the
same question, record the verified answer immediately after resolving it, before
continuing the surrounding task. This includes very small facts. Do not defer the
work to a documentation pass or suppress leaves to keep the file count low.

The operating loop is lookup -> discover -> verify -> record -> use. On every miss,
find an existing semantic owner and update it, or create a suitably scoped leaf using
contextual judgment. If the answer remains blocked but the question is reusable,
immediately create a truthful
`status: unresolved` leaf recording `checked_at`, the blocker, and the next check.
If writing is forbidden, leave a scoped handoff.

One exact question and direct answer per leaf is often useful guidance, but never an
automatic rule. Atomicity is about retrieval meaning, not textual size. A reasoning
agent should decide whether related knowledge belongs together or apart in context,
considering its degree of relation, likely queries, expected joint use, ownership,
volatility, proofs, review triggers, branch fan-out, tool calls, metadata, drift, and
reconstruction cost. These considerations inform judgment; none independently
dictates a split or consolidation.

Canonical orientation and repository spine leaves are deliberate aggregation points.
`where/am/i.md` and `what/is/the/spec.md` may contain many facts because their broad
questions require an orienting or governing projection. `what/is/the/plan.md`,
`what/is/the/state.md`, and `what/is/next.md` similarly project coordinated current
truth. Controlled repetition of key facts in these projections is useful; detailed
semantic leaves still provide targeted retrieval. Do not thin the projections into
link catalogs or inflate them with unrelated archival detail.

Before choosing an ordinary semantic path, write
the full natural-language question the leaf answers. Form the semantic path by
lowercasing it, removing only punctuation that is not part of a literal identifier,
replacing every space with `/`, and adding `.md` to the final word. Keep grammatical
words such as `to`, `is`, `the`, `of`, and `for`: they make the path read as the
question when `/` is spoken as a space. For example, "how to check knowledgetree
proofs" becomes `how/to/check/knowledgetree/proofs.md`. If that slash-expanded path
does not read roughly as the complete question a future agent will ask, the path is
wrong. When one semantic path component genuinely contains multiple words,
hyphenate those words; for example, use `known-good`, never `known_good`. The
`snake_case` convention for code identifiers does not apply to knowledge-tree paths.
A hyphen joins words within one semantic choice; it must not compress distinct
sentence choices or omit grammatical words. Do not invent category buckets,
implementation-shaped nesting, or compressed noun piles in place of the sentence.

Record the conclusion and the distinction that made it non-obvious, not task
chronology or stream of consciousness. A healthy corpus is expected to have a
heavy-tailed length distribution: many short leaves, fewer medium leaves, and a small
number of long cohesive leaves, roughly inverse-rank or more strongly decaying. This
is a design heuristic, not a size quota. File count has real traversal, filesystem,
version-control, metadata, and gardening costs. Improve branch shape when navigation
becomes ambiguous; do not combine clearly independent answers merely to avoid files
or fragment a cohesive answer merely to maximize atomicity.

## Ingesting legacy knowledge

When replacing a document corpus, inventory the source only as much as needed to
establish a coverage boundary, then process it section by section. For every
substantive statement, decide whether it is a requirement, decision and rationale,
procedure, interface contract, current-state fact, failure mode, acceptance gate, or
other reusable answer. Put independently retrievable answers in independent leaves;
cross-link shared facts instead of duplicating them.

Do not copy a source document wholesale into one leaf, preserve it as the canonical
answer, or create leaves whose useful content is only a source path. Provenance may
name an ingestion source, but the leaf body must contain the answer. A summary leaf
does not establish coverage of omitted details.

Before retiring a source corpus, check each substantive section against actual leaf
answers, resolve contradictions against the governing authority and current primary
evidence, and ensure no reusable fact exists only in the source. Then remove the
redundant corpus and repair references that would otherwise point to it. The desired
end state has one knowledge authority, not synchronized old and new documentation.

When agents assist with ingestion, give each worker one short section, one semantic
question, one contradiction check, or another independently reviewable crumb. State
exact read and write boundaries. The coordinating integrator decides relevance,
atomicity, branch shape, authority, deprecation, portability, and final coverage.
Continue non-overlapping integration work while a worker runs; do not turn delegation
into idle waiting.

Put reusable personal and host knowledge in `~/.knowledge`; put project facts,
local procedures, architecture, policy knowledge, and current project state in the
active project's nearest `.knowledge` root. Never promote professional, customer,
partner, or other restricted knowledge into the global tree.

Write the answer first, then only the context, preconditions, limitations, eligible
proofs, and links required to use it. Link to one canonical answer from alternate
routes instead of copying it. Every verified leaf must include `verified_at` (ISO
8601 with timezone), `verified_by`, `scope`, `source`, `verification`, and
`review_when`; put these beneath `metadata` when the leaf is also a `SKILL.md`. Name
the evidence actually checked and never overstate verification.

Maintain current truth in place. Before replacing a leaf, reread it to avoid
overwriting concurrent work. Correct stale or conflicting answers, update affected
orientation, and remove superseded current state; Git retains history. Commit
project-local knowledge with its owning code when repository policy permits. Do not
automatically publish global personal knowledge.

Before finishing any task, ask what you had to determine that a future agent should
not have to determine again. Confirm those answers were already captured, their
proofs run where applicable, metadata and scope are truthful, canonical root
components exist in the active scope, no non-leaf payload files exist, and a
representative sentence-derived semantic route works. Rerun the relevant semantic
token checks at the final important junction.
For repository work, completion additionally requires refreshed
`what/is/the/state.md` and `what/is/next.md`; do not claim the task is complete until
both describe the post-task reality.

Knowledge records evidence and procedure; it does not create execution authority or
resurrect superseded requirements. Current higher-authority instructions always
govern.

The global semantic leaves under questions such as `what/is/a/knowledge/tree.md`,
`how/should/an/agent/traverse/a/knowledge/tree.md`,
`how/should/legacy/documents/be/ingested/into/a/knowledge/tree.md`, and
`how/should/knowledge-tree/work/be/delegated.md` contain independently retrievable
answers and rationale. This skill restates only the mandatory operating protocol
needed by agent harnesses that still bootstrap through skills.
