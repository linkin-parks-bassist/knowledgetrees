# Knowledgetrees

*Agentic knowledge as a categorical limit corpus with skeptical intuitionistic sub-verification*

Knowledgetrees are a stateful, self-growing, self-healing filesystem for
agent knowledge. They aim to replace the split between skills, documentation, code
comments, project memory, plans, specifications, working policy, and operational
notes with one canonical, agent-navigable substrate.

The idea is simple: store useful knowledge in meaningful filesystem paths, let
agents fetch only the answers they need, and make ordinary work continuously improve
the knowledge available to the next agent.

**Knowledge is discovered as needed and captured as learned.**

This repository contains:

- a visible, self-describing public corpus in [`example/`](example/where/am/i.md);
- the knowledge-first [`install`](install) script;
- the standalone [`verify-knowledgetree-proofs`](tools/verify-knowledgetree-proofs)
  verifier; and
- selected planning and specification practices distilled into semantic leaves,
  without inheriting an inflexible skill-driven workflow.

## Two roots, two jobs

This repository intentionally contains two different semantic trees:

| Path | Role |
| --- | --- |
| [`.knowledge/`](.knowledge/where/am/i.md) | The real operational knowledge root for developing and publishing this repository. It contains this project's requirements, plan, current state, and next action. |
| [`example/`](example/where/am/i.md) | The visible distributable example. It contains public, reusable knowledge-tree methodology and illustrative planning/specification leaves. |

They are not mirrors. Repository-specific facts belong only in `.knowledge/`.
Reusable public example knowledge belongs only in `example/`. Agents working on
this repository orient through `.knowledge/` first.

### Make the example yours

[`example/where/am/i.md`](example/where/am/i.md) is intentionally empty. Fill it in
with an orientation to your own local environment: what scope the tree covers, the
repository or workspace purpose, important topology, active priorities, relevant
tools, operational boundaries, and the semantic routes an agent should try first.
Write enough that a fresh agent can orient without recursively inventorying the
workspace.

Describe what each branch holds and include real leaf paths, not just a branch
list. Route planning to `how/to/make/a/plan.md`, for example, and clarification to
`when/to/ask/clarification.md`.

Keep the orientation current and useful, but do not put passwords, tokens, private
keys, or other secrets in it. If the tree will be published, also remove personal or
organization-specific details that should not become public.

## A filesystem that doubles as an ontology

A knowledgetree is usually a `.knowledge/` directory. Its paths are not arbitrary
folders: they are meaningful questions and concepts. The structure itself helps an
agent retrieve the answer.

```text
.knowledge/
├── where/
│   └── am/
│       └── i.md
├── what/
│   └── is/
│       ├── the/
│       │   ├── spec.md
│       │   ├── plan.md
│       │   └── state.md
│       └── a/
│           └── knowledge/
│               └── tree.md
├── how/
│   └── to/
│       ├── check/
│       │   └── knowledgetree/
│       │       └── proofs.md
│       └── make/
│           └── a/
│               └── plan.md
├── when/
│   └── to/
│       └── ask/
│           └── clarification.md
└── why/
    └── is/
        └── a/
            └── knowledge/
                └── tree/
                    └── not/
                        └── an/
                            └── index.md
```

If an agent needs to know how to make a plan, it can predict
`how/to/make/a/plan.md`. If it needs to understand why a knowledge tree is not an
index, it can descend through `why/is/a/knowledge/tree/not/an/index.md`. LLMs are
fundamentally language models. With knowledgetrees, if an agent has a question,
*the question itself can point directly at the answer*. The path is already half
the retrieval query. This is not merely documentation stored in folders: every
branch narrows what the agent is asking, and the leaf directly answers the question.

An agent does not need to word a question exactly like the answer's path. In early
use, nearby semantic components give agents enough structure to choose a likely
branch and narrow in quickly when the first guess is not exact.

Further testing is required to see how this behaves at larger scales. As long as
branches remain meaningfully discriminating, each path choice reduces the search
space without loading the whole corpus.

## Why it matters

Agent context is expensive, fragile, and temporary. Useful knowledge is commonly
scattered across giant instruction files, README pages, skill blobs, chat history,
plans, notes, and source comments. Agents repeatedly load too much, miss the right
thing, or rediscover facts that another run already worked out.

Knowledgetrees change that trade-off:

- **Less prompt bloat.** Detailed knowledge can exist in abundance without being
  injected into every run. Its cost is paid only when needed.
- **Survives fresh starts.** A new worker, compacted session, or different model can
  reconstruct context from persistent current knowledge.
- **Current truth wins.** The canonical state is updated rather than forcing a model
  to infer which paragraph in a chronology is newest.
- **Knowledge compounds.** Every reusable discovery can save a future reasoning
  loop, failed command, search, or architectural mistake.
- **One substrate, many uses.** The same tree can carry build procedures, policy,
  architecture, plans, specs, environment facts, and rationale.
- **Composable by design.** An agent can retrieve a general rule, local refinement,
  current state, and rationale separately, then combine only what applies.

The familiar stack is fragmented:

| Traditional surface | Typical role |
| --- | --- |
| `AGENTS.md` | Global instructions and project quirks |
| `skills/` | Procedures the model must remember to select |
| `docs/` | Linear presentations with buried answers |
| code comments | Design rationale tied to where the implementation happens to live |
| `plans/` and `specs/` | Current intent, often duplicated elsewhere |
| notes and chat history | Discoveries mixed with obsolete chronology |

A Knowledgetree gives those concerns one distributed, versionable semantic
environment. The agent asks a question, retrieves the current answer, follows
related leaves only when necessary, and preserves better knowledge when it learns
something reusable.

Store knowledge. Generate presentations. Do not make every future agent reread the
presentation to recover the knowledge.

### Even code comments

Skills. Documentation. Code comments. The same knowledge, trapped in three
different retrieval conventions. Why should an agent have to discover the right
source file and scroll to the right comment to understand a design decision?

With `why/does/this/function/do/that.md`, the question itself becomes the retrieval
route. Constraints, rejected alternatives, invariants, and strange-looking choices
become maintained knowledge—with provenance, scope, and executable proofs wherever
the facts are mechanically verifiable. The code shows what happens; the tree
explains why.

Comments can be stored separately to code, and retrieved as needed - keeping the
codebase itself compact, saving precious tokens, while (arguably) leaving the code
even *more* accessible... to agents.

## What makes it different

This is not a search system bolted onto documentation. The tree itself is the
primary agent-facing knowledge representation. Documents can still exist as
external authorities, evidence, source material, exports, or human-facing views.

### The tree contains answers, not just pointers

“The refund policy is in `customer-guide.pdf`” is weak knowledge. A useful leaf
states the current policy directly, links to the governing source if necessary, and
says when to check it again.

### Current state is mutable; history is separate

When a policy changes, amend its current semantic owner. Keep the old version in Git
or explicit history when history still matters. Do not make the next agent reason
over incompatible versions and guess which governs.

### Knowledge is federated

A user-wide tree can carry reusable tooling and host knowledge; a project tree can
carry local policy and architecture; a subsystem can carry narrower context. The
nearest applicable knowledge is consulted before broader knowledge.

Knowledge trees can live in **any directory**. A repository should have a repo-wide
`.knowledge/`, and subfolders can—and should, when they have their own useful
context—have narrower trees too: `frontend/.knowledge/`, `backend/.knowledge/`, or
even `backend/payments/.knowledge/`. This is another dimension of compositionality:
directory scope selects relevant knowledge before semantic paths narrow the question.
An agent working on payments gets payment-specific answers at its fingertips,
without polluting its context with unrelated frontend knowledge. Broader roots still
supply shared facts; narrower roots own their local refinements.

### Growth is ordinary maintenance

When an agent has to determine something, it asks whether a future agent would have
to rediscover the answer. If so, verifying and preserving it is part of finishing
the work—not a documentation chore deferred until later.

### Concrete facts can reconnect themselves to reality

Agents are encouraged to attach small executable proofs to factual claims that are
immediately and mechanically verifiable:

````markdown
The repository has a local orientation leaf.

Proof: (verified at _)

```bash
test -f .knowledge/where/am/i.md
```
````

The goal is not to turn every sentence into code. Proofs are for single, immediately
checkable true-or-false assertions—not requirements, instructions, opinions, plans,
or compound conclusions.

**Agents run the verifier before relying on proof-backed knowledge.** They check the
active root during bootstrap and when entering a new scope, then relevant semantic
slices before consequential use. A broken proof is a stop-and-repair signal: inspect
the evidence, correct or remove the stale assertion or faulty predicate, and rerun
the check before using that knowledge.

This gives the schema a layer of executable provability: eligible facts reconnect
to reality instead of remaining unchecked prose. A passing verifier establishes
that the marked predicates passed—not that every unproved statement is true.

Each passing proof refreshes its own `Proof: (verified at …)` marker with an ISO
8601 timestamp. Failed proofs receive `Proof: (falsified at …)` and set the leaf's
`falsified_at` metadata. That flag requires independent review to clear: even if
every proof later passes, the leaf remains falsified and the verifier reports it.
Passing every proof is necessary but not sufficient for leaf validation.
Leaf-level `verified_at`
is separate and changes only after an independent review of the whole leaf; the
verifier does not infer whether every statement is covered by proofs. Use
`--no-stamp` when a read-only check is needed.

Run every marked proof in this repository with:

```bash
tools/verify-knowledgetree-proofs --root example
```

Run a semantic slice by passing exact path-component tokens:

```bash
tools/verify-knowledgetree-proofs --root example knowledge-tree proofs
```

Multiple tokens select their disjunction. Use `--verbose` for per-leaf diagnostics.

The operating loop is:

```text
lookup → discover → verify → record → use
```

## Policy, procedure, and state compose naturally

Instead of one giant deployment manual, independent concerns can remain
independently owned:

```text
how/to/release/software.md
how/to/release/the/web-app.md
how/to/verify/a/release.md
what/is/the/current/release/channel.md
where/is/the/staging/environment.md
why/does/production/require/two-approvals.md
```

A release worker can assemble the pieces relevant to its situation without forcing
every other task to ingest the entire release universe. General procedure,
environment-specific refinement, current state, and rationale can change
independently and compose at the point of use.

## A self-improving documentation methodology

Traditional documentation decays because writing it is a separate activity. A
knowledgetree makes maintenance part of normal agent work.

| Traditional pattern | Knowledgetree pattern |
| --- | --- |
| Agent searches documents | Agent follows the semantic tree to the current answer |
| Agent discovers a missing fact | Agent verifies and records it at the right scope |
| Documents become stale | Leaves carry provenance, review triggers, and eligible proofs |
| Documentation is linear | Knowledge is addressed by question and assembled on demand |
| One giant guide | Focused answers plus deliberate orientation and spine projections |
| Skills are separate blobs | Procedures share a namespace with their facts and policies |

The long-term effect is cumulative: what one agent learns becomes part of the
environment in which the next agent thinks.

## Deliberately ordinary machinery

The mechanism does not require a vector database, graph store, ontology language,
memory server, or new agent protocol. It starts with files, directories, Markdown,
links, normal version control, and ordinary tooling.

- **Versionable.** Code and knowledge can change atomically in the same commit.
- **Human-readable.** Any leaf opens in an ordinary editor.
- **Extensible.** Routing models, embeddings, proof schedulers, and gardening agents
  can be added later without changing the basic abstraction.

### Hard obligations

- Use applicable knowledgetrees during ordinary agent work.
- Keep paths semantic and traversable.
- Store useful answers, not merely directions to internal documents.
- Maintain current truth instead of relying on chronology.
- Preserve reusable discoveries immediately.
- Verify eligible base facts proportionately.
- Keep knowledge separate from execution authority.

### Contextual judgments

- Whether a topic needs one leaf or several.
- Whether a leaf should be short or substantial.
- Whether to split or consolidate related material.
- How much controlled repetition belongs in orientation.
- Whether direct reading, listing, or search is the cheapest retrieval method.
- How a mature tree should be reorganized as it grows.

Rigor belongs in the obligations. Flexibility belongs in the organization.

## Install

The installer asks `[n/Y]` before configuring OpenCode permissions. The warning
discloses automatic reads of `~/.knowledge/**` and `~/.agents/**`, automatic writes
to `~/.knowledge/**`, and that read contents may reach the configured model
provider. Edits to `~/.agents/**` still require approval. Declining cancels before
any installation changes; an existing matching configuration needs no new grant.

New installations get a navigation starter in `where/am/i.md`; add your verified
local environment facts and concrete routes. Existing orientations are preserved.

Run the installer from a clone:

```bash
./install
```

The installer is knowledge-first. It safely merges the reusable leaves from
`example/` into `~/.knowledge`, preserves an existing `where/am/i.md`, installs the
single verifier at `~/.knowledge/.tools/verify-knowledgetree-proofs`, and adds the
mandatory once-per-session bootstrap to `~/AGENTS.md`. The loaded procedure remains
active across messages and tasks; it is not reinvoked on every turn. The installer
refuses to overwrite differing knowledge unless `--force` is supplied explicitly.
Preview its work with `./install --dry-run`.

Installation also puts `kt` in `~/.local/bin` (add that directory to your `PATH`
if needed). Use `kt find leaves` or `kt find "how to add knowledge leaves"` for
ranked keyword results, `kt open global:how/to/add/knowledge/leaves.md` to read a
leaf verbatim, and `kt proof --no-stamp leaves` to check relevant proofs.
`kt roots` shows the active scopes. Search is lexical, not a semantic model;
scores rank matches, and a miss does not prove knowledge is absent.

Question prefixes make the directories active search boundaries:
`kt where is vivado` walks `where/is/` and returns the exact leaf if present.
Otherwise, it walks matching directory words until the first mismatch and ranks
the remaining keywords only among that branch's descendants. Weak matches cause
it to climb one parent and search wider. `kt how to _` lists a procedure branch.
Use `where/is/` for locations, `how/to/` for procedures, `when/to/` for triggers,
`what/is/` for definitions/state, and `why/does/` or `why/is/` for rationale.
`kt find` remains the deliberately broad search interface.
Keyword lookups exit `1` for empty or weak-only results, even when suggestions are
shown; `0` means a candidate passed the heuristic, not that its answer was verified.
The default threshold is 60% coverage of non-grammatical query keywords; tune it
with `--min-coverage`. Exact-path reads and explicit branch listing remain distinct.

Capture a new answer in one call:

```sh
kt add "how to prepare the demo" "Run the project's documented demo command." --source "checked project instructions"
```

`kt capture` works too. The full question becomes `how/to/prepare/the/demo.md`.
Capture defaults to the nearest project tree, otherwise global; select `--global`,
`--project`, or `--root example` explicitly. Use `--scope` for a scope description,
`--dry-run` to preview, or `-` as the answer to read multiline Markdown from stdin.
Existing leaves are protected: read their owner and amend deliberately.
New leaves receive a creation timestamp and `status: unverified`, not an invented
verification claim. Capture neither executes nor manufactures proofs. Independently
review the whole answer and check eligible proofs before relying on it.
For unresolved answers, add `--unresolved --blocker "missing evidence" --next-check
"specific next investigation"`; the record receives a separate checked timestamp.

The agent default is **new question → `kt` first**, unless adequately checked
knowledge is already loaded. If `kt` does not find the information, the agent must
determine whether a leaf exists using alternate terms and scoped semantic inspection.
Existing leaves are read or amended; absent leaves must be added after investigation,
or recorded as unresolved when blocked. Capture an established answer before the
next unrelated tool call or completion—not in a later documentation pass.

### Failure and capture-review hooks

The installer adds reminders for **Codex, OpenCode, and GitHub Copilot CLI**:

- After a detected tool failure, check `kt` for a known explanation or fix. Once
  the cause is understood, capture the reusable diagnosis or amend its owner.
- At task end, a failure or 10 completed tool calls requests one capture-review
  follow-up. The agent checks existing owners and records missing discoveries,
  or reports that there is nothing new to retain.

Codex uses `PostToolUse` and `Stop`; Copilot CLI uses `postToolUse`,
`postToolUseFailure`, and `agentStop`; OpenCode uses a local plugin and
`session.idle`. Existing unrelated hooks are preserved. In Codex, open `/hooks`
and review/trust the installed definitions; new hooks are skipped until trusted.
Restart OpenCode to load its plugin, and start a new Copilot CLI session.

Set `KT_HOOK_MIN_CALLS` in the harness environment to change the activity threshold.
Session-isolated counters and hashed event receipts live under
`${XDG_STATE_HOME:-~/.local/state}/knowledgetrees`, not inside tree payloads.
They store no raw commands, tool outputs, passwords, or knowledge contents.
Reviews can consume an extra model turn. A one-shot guard prevents the review
from recursively waking itself; the next ordinary user prompt starts a new cycle.
These are reliability reminders, not semantic capture verification or a security
boundary. Failures need detectable result status; arbitrary prose errors cannot
always be recognized. They do not grant permissions or automatically write leaves.

Existing installations can update the CLI and hooks without replacing their leaves:

```sh
./install --hooks-only --force
```

Preview with `--dry-run`. Use `--no-hooks` during installation to skip hook setup.
The handler and OpenCode adapter need only Python 3 and the harness's existing JS
runtime. See [the hook procedure](example/how/to/use/knowledgetree/hooks.md) for
event contracts and limitations. This integration targets local Copilot CLI;
Copilot cloud jobs and VS Code need their own environment/distribution setup.

### Why did skills appear after installation?

After installation, Codex and other harnesses may appear to contain a
`knowledgetrees` skill. Current agent harnesses still require a skill-shaped entry
point to start the procedure, so the installer creates one as compatibility
plumbing—not as another knowledge store. After installing the canonical procedure at
`~/.knowledge/how/to/use/knowledgetrees.md`, the installer creates
`~/.agents/skills/knowledgetrees/SKILL.md` and
`~/.codex/skills/knowledgetrees/SKILL.md` as hard links to that same file. All three
paths share one inode: there is no wrapper and no second body to drift.

The installer also exposes four focused skills in both harness directories:
`knowledgetrees-lookup`, `knowledgetrees-capture`, `knowledgetrees-maintenance`,
and `knowledgetrees-ingestion`. Each `SKILL.md` hardlinks to its corresponding
canonical procedure leaf in the global KT. Their descriptions advertise when to
use them, while the bootstrap keeps its kt-first and miss-resolution rule inline
and remains once per fresh session. Detailed knowledge is still stored and
maintained in the tree.

Quit and restart OpenCode and Codex after installation or an upgrade so their
startup-loaded skill catalogs refresh; an already-running conversation may retain
older descriptions or procedure content.

## A minimal adoption path

1. Create `.knowledge/where/am/i.md` and the canonical `how/`, `what/`, `where/`,
   and `why/` branches.
2. For repositories, create current-truth spine leaves for the spec, plan, state,
   and next action.
3. Project frequently needed answers into paths that read as natural-language
   questions.
4. Teach agents to retrieve from and continuously maintain the tree.
5. Add proofs only where a concrete fact is cheap and safe to check.
6. Garden ambiguous branches, stale answers, duplication, and fragmentation when
   actual use exposes friction.

## Common questions

### Is this just RAG with folders?

No. RAG usually treats documents as the primary corpus and retrieves chunks from
them. A knowledgetree makes the maintained semantic answer the primary artifact,
with the path participating in retrieval. Search remains a fallback.

### Does every fact need its own file?

No. The design favors useful semantic boundaries, not maximum file count. Closely
related material can stay together, and orientation, spec, plan, and state leaves
are deliberate aggregation points.

### Does this mean deleting all normal documentation?

No. External governing documents, published manuals, and human deliverables may
remain important. The internal agent-facing source of reusable knowledge should be
structured as knowledge first. Human presentations can be generated or frozen when
needed.

### Does a knowledgetree replace task management?

No. It provides knowledge continuity. Work still needs bounded objectives,
authority, ownership, acceptance criteria, and runtime lifecycle.

### What happens when a proof fails?

Stop trusting the claim. Determine whether the fact is stale, the predicate is
broken, or the check could not run. Then update or mark the knowledge accordingly. A
failed implementation check does not automatically rewrite a requirement.

## Methodology provenance

The visible `example/` tree is adapted from a working global knowledgetree. Host paths,
personal facts, private state, and local experiment history have deliberately been
excluded. The planning, specification, update, and clarification leaves distill
generally useful ideas from the MIT-licensed
[Superpowers](https://github.com/obra/superpowers) 6.3.0 methodology; they are not
copies of its skill-era process or mandatory approval gates.

## Installer guarantees

The installer is covered by an isolated-home integration test. It verifies that:

- reusable knowledge is installed without importing the example's illustrative
  spec, plan, state, or next-action leaves;
- an existing orientation, `AGENTS.md`, and Codex configuration are preserved;
- repeated installation is idempotent;
- differing knowledge is rejected before overwrite unless `--force` is explicit;
- the verifier runs successfully from its single global installation; and
- both compatibility `SKILL.md` paths have the same device and inode as the
  canonical installed procedure.

Run the checks with:

```bash
python3 -B tests/test-install.py
```

## The proposal in one sentence

Make the filesystem remember what agents learn.

A knowledgetree is a distributed, stateful knowledge environment in which
paths encode meaning, agents discover current answers on demand, procedures and
policy compose with project state, mechanically checkable facts can revalidate
themselves, and every useful piece of work has the opportunity to make the next
piece of work easier.

**Knowledge is discovered as needed and captured as learned.**
