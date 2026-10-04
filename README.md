# Knowledgetrees

Knowledgetrees give agents a maintained filesystem of current answers. Store
knowledge in paths that read as questions, retrieve the answers needed for the
work, and advance those answers as implementation, requirements, decisions, and
facts change.

**The tree remembers what is true, not what happened.**

A leaf contains the best direct answer now. Rewrites reconsider the whole answer
and remove superseded material; Git owns chronology. The tree is the sole
maintained knowledge source for its scope. Code and external documents supply
evidence, while READMEs, manuals, and other presentations can be derived from it.

Knowledge trees cover every scale: function contracts and rationale, typedefs,
include order, dependencies, build procedures, architecture, policy, complete
specifications, and plans. No useful answer is too fine-grained. A fresh agent can
retrieve that knowledge without reconstructing it from previous conversations.

This repository ships a standard-library Python CLI, a 23-tool MCP server, startup
and maintenance adapters for **Claude Code, Codex, OpenCode, and Copilot CLI**, an
installer, regression tests, and reusable guidance in [`example/`](example/).

## Install and start a tree

From a complete clone, preview installation and then install:

```bash
./install --dry-run
./install
```

The installer merges reusable guidance into `~/.knowledge`, installs the CLI and
MCP server under `~/.knowledge/.tools/`, and links `kt` into `~/.local/bin`. Add
`~/.local/bin` to your `PATH` if needed. It installs startup and turn-end hooks and
registers the MCP server with all four harnesses. If the Claude CLI is absent, it
prints the manual registration command.

Existing orientations, unrelated configuration, other MCP servers, and existing
`knowledgetrees` registrations are preserved. The example's illustrative spec and
plan are excluded. Differing managed files require explicit `--force`; inspect
the differences first. Even with `--force`, an existing orientation is preserved.
The installer removes its legacy managed `~/AGENTS.md` block and preserves any
other contents.

Before changing OpenCode permissions, the installer asks for informed `[n/Y]`
consent. It discloses automatic reads of `~/.knowledge/**` and `~/.agents/**`,
automatic writes to `~/.knowledge/**`, and possible exposure of retrieved content
to the configured model provider. Edits to `~/.agents/**` remain approval-gated.
Declining or EOF cancels before installation changes.

| Option | Effect |
| --- | --- |
| `--dry-run` | Preview targets and conflicts without writing |
| `--force` | Replace differing managed files, preserving orientation |
| `--hooks-only` | Refresh CLI, hooks, and MCP infrastructure in an existing installation without replacing leaves or skills |
| `--no-hooks` | Skip hook installation; existing hooks remain |
| `--no-mcp` | Skip MCP deployment and registration |
| `--home PATH` | Select a target home directory |

Restart your harness after installation or upgrades so it loads the new tools,
hooks, and skill catalog. See [installation details](example/how/to/install/knowledgetrees.md).

In the directory whose knowledge you want to maintain:

```bash
kt init
# Alternatively, for a repository with a spec and remaining-work plan:
# kt init --project
```

Choose one form. Both create `.knowledge/` with empty `how/`, `what/`, `where/`,
`why/`, `does/`, and `is/` branches plus `where/am/i.md`. The project form also
creates empty `what/is/the/spec.md` and `what/is/the/plan.md`. An optional
`ORIENTATION` argument becomes the literal orientation contents. Initialization
refuses an existing tree and registers the new root under `ask`, without granting
cross-project access.

Fill the orientation with the scope, purpose, topology, boundaries, and actual
semantic routes of your environment. Describe what each branch holds. Keep the
specification as the acceptance contract and the plan as **remaining steps, next
first**; remove completed steps immediately. Add verified answers as work exposes
a need for them, and attach proofs where a fact is cheap and safe to check.

## Questions become paths

A tree's paths express what an agent is asking:

```text
.knowledge/
├── where/am/i.md
├── what/is/the/spec.md
├── what/is/the/plan.md
├── how/to/build/the/project.md
├── when/to/ask/clarification.md
├── why/does/the/parser/reject/empty/input.md
├── does/the/installer/preserve/configuration.md
└── is/the/cache/shared.md
```

The last five paths illustrate answers you might establish in your own tree.
Each leaf directly answers its question, with evidence, qualifications, and links
where useful. A pointer such as “the answer is in a large internal document” does
not replace the answer.

| Question | Branch |
| --- | --- |
| Where is …? | `where/is/` |
| What is …? | `what/is/` |
| How to …? | `how/to/` |
| When to …? | `when/to/` |
| Why does/is …? | `why/does/` or `why/is/` |
| Does …? / Is …? | `does/` or `is/`, with a qualified yes/no answer |

Exact question paths return whole answers. Otherwise, `kt` consumes matching
path words, ranks remaining keywords within that branch, and widens one parent
at a time when matches are weak. Retrieval is lexical, not a semantic model; the
default threshold is 60% meaningful-keyword coverage. A successful match is a
candidate, not a correctness certificate. A miss does not establish absence.

Agents use **new question → kt first**, unless adequately checked knowledge is
already loaded. On a miss, they retry useful terms and inspect plausible paths to
find an existing owner. They then read or repair that owner, or investigate and
establish an absent answer before unrelated work. A blocked answer records its
blocker and next check. This prevents duplicate owners and repeated rediscovery.

Leaves can be short or substantial. Choose boundaries by how answers are used,
owned, and reviewed; orientation, spec, and plan deliberately aggregate related
knowledge. General procedure, project policy, local facts, and rationale can be
retrieved separately and composed for the task.

## Tools for agents

When MCP tools are available, agents use them in preference to the shell. The
server delegates knowledge semantics to the CLI, keeping access, revisions,
lifecycle, and proofs consistent. MCP names may carry a harness prefix such as
`mcp__knowledgetrees__kt_lookup`.

| Job | Tools |
| --- | --- |
| Find | `kt_lookup`, `kt_find`, `kt_grep`, `kt_dict`, `kt_roots` |
| Read | `kt_read`, `kt_info` |
| Change | `kt_add`, `kt_rewrite`, `kt_undo`, `kt_rm`, `kt_mv`, `kt_combine`, `kt_init`, `kt_register` |
| Check | `kt_renew`, `kt_prove`, `kt_status`, `kt_audit` |
| Access | `kt_access_status`, `kt_access_request`, `kt_access_confirm`, `kt_access_revoke` |

`kt_add`, `kt_prove`, `kt_status`, and `kt_audit` can target an approved root
directly. Useful discovery, inspection, and access results include structured
content. Four MCP prompts—`frontier_review`, `garden`, `verify_leaf`, and
`revoke_access`—appear as slash commands where supported.

A whole-leaf MCP read returns the complete answer and `Revision: HASH`, hiding
front matter and timestamps. Only yellow or brown leaves carry a leading notice.
There are no partial reads, ranges, paging, or truncation. Search excerpts select
candidates; they are not reads and supply no rewrite hash.

Growing an answer beyond 1,000 body words triggers two rejected writes asking for
whole-leaf reconsideration, or three when the larger current/proposed body exceeds
2,000 words. Remove stale, irrelevant, or log-shaped content while preserving valid
knowledge. A short or shorter answer passes immediately; remaining growth can pass
after the bounded rejections. Rejections leave the leaf and revision untouched
(CLI exit 5; MCP tool error). Counters persist across calls outside the tree and
reset when its committed revision changes. Dry runs, unchanged no-ops, and
metadata-only changes consume no attempts. Length is a pressure signal, not a
diagnosis of stale knowledge.

`kt_rewrite` replaces the complete answer using the SHA-256 revision from a whole
read or successful rewrite. It can also set or clear expiry and verifiability
metadata. The old answer is material to reconsider, not a template to extend.
Stale revisions fail under the write lock. Successful rewrites return a diff and
committed `Revision: HASH`, including no-ops; reuse it for the next rewrite
without rereading. A conflict requires a fresh read and merge. Dry runs return
only a preview.

`kt_renew` attests that the **whole answer** was checked against current evidence
and reruns its proofs. It requires a whole read or successful rewrite in that MCP
session, with no intervening change. A known hash alone is not that attestation.
See [MCP design and limits](example/how/to/expose/structured/knowledge-tree/edits/across/local/agent/harnesses.md).

## Verification and maintenance

Executable proofs connect concrete claims to current evidence:

````markdown
The repository has a local orientation leaf.

Proof:

```bash
test -f .knowledge/where/am/i.md
```
````

Use the exact timeless `Proof:` marker and a small, bounded, read-only predicate
that returns zero exactly when the preceding claim is true. Proofs are for
concrete assertions, not policy, plans, instructions, or opinions. Repository
behavior can be backed by focused regression tests. Proof execution does not
certify unproved prose, agreement between leaves, or adequate coverage.

| State | Meaning and required action |
| --- | --- |
| Green | No current lifecycle warning; check evidence and scope before reliance. Proof-free leaves can be green. |
| Yellow | Review is due; verify the whole answer, repair if needed, and renew before use. |
| Brown | A falsification, failed or malformed proof, or invalid metadata requires a priority-one incident response. |

**Brown stops unrelated work, including at startup.** The agent first prominently
reports the affected leaf, then diagnoses the mismatch, chooses the safest
remediation, repairs the answer or proof, independently reviews the whole answer,
renews when required, and rechecks. If safe remediation cannot be established, it
asks the user for guidance. Only explicit permission to ignore that specific
brown status permits other work; it does not validate or green the leaf.

Nonempty leaves use flat Markdown front matter. `revised_at` records content
changes; `checked_at` records manual whole-answer review. Optional `expires_at`
or `expires_every` sets a review boundary for volatile claims. Do not add arbitrary
expiry to durable architecture, rationale, specifications, or plans. Supply answer
bodies to add/rewrite; the tools manage metadata.

A normal CLI proof run stamps lifecycle status and only lowers it. MCP
`kt_prove` is read-only unless `stamp: true`; CLI `--no-stamp` also preserves
bytes. Manual renewal is the way back up, with one reviewed exception:
`verifiable: true` asserts that the leaf contains only concrete facts and every
claim is covered by its proofs. Such a leaf needs at least one proof; all proofs
running and passing auto-green it, including sticky falsification. Missing,
malformed, skipped, or failed proofs make it brown. The author must verify
coverage; the engine cannot detect an uncovered sentence.

`kt status` lists non-green leaves without executing proofs. `kt audit` separately
flags bodies over 1,000 words as `suspect` and date-shaped bodies as
`quite-suspect`. Audit is read-only: these are review signals, not diagnoses or
lifecycle states. Dates in current schedules, queues, events, machine state, and
protocol identifiers may be legitimate.

Maintenance happens alongside ordinary work. If checked evidence contradicts a
leaf, repair its owner and affected guidance before relying on it. After a
behavior change, inventory narrow and broad owners, specifications, plans,
orientation, public examples, README/help, hooks, and generated or installed
copies. Search for both the new behavior and superseded claims, read relevant
hits, and reconcile them. Tests, green proofs, and matching installed bytes
support this semantic review; none substitutes for it.

## Startup and turn-end hooks

Startup hooks inject **proof-free** `kt --lean info --no-prove` output: the
canonical procedure, accessible ancestor orientations from `~` down to the
working directory, and the path dictionary. They direct the agent to call
`kt_prove` for the exact local root before other work, or global when no exact
local tree exists. Project proof commands run through agent tooling, never inside
the startup hook. Direct `kt info` still includes the proof result; consume its
complete output.

| Harness | Startup | Maintenance |
| --- | --- | --- |
| Claude Code | `SessionStart` | `Stop` |
| Codex | `SessionStart` | `Stop` |
| OpenCode | System-context plugin | `session.idle` |
| Copilot CLI | `sessionStart` | `agentStop` |

Resume, clear, and compaction refresh startup context where supported. Above
9,500 bytes, Claude Code receives an instruction to call `kt_info` directly
instead of oversized injected context; `KT_HOOK_CONTEXT_LIMIT` tunes that
threshold. Accessible ancestor orientations provide context without adding those
trees as lookup roots or widening access.

The turn-end hook asks for one frontier-maintenance pass, at most once per five
minutes per session (`KT_HOOK_MAINTENANCE_INTERVAL`, default 300 seconds). Where
transcript support exists, it skips turns that already maintained the tree after
the last edit; Copilot uses the rate limit alone. The continuation asks the agent
to reconcile affected answers, establish missing owners, review status and audit
signals, and remove completed plan steps. It never edits knowledge itself, grants
no authority, prevents reminder loops, and fails open on hook errors.

Claude Code maintenance delivery has been observed live. Fresh-harness checks of
the installed MCP/access flows and startup brown response, plus live maintenance
delivery in Codex, Copilot CLI, and OpenCode, remain validation work. Protocol and
adapter tests do not establish that a running client loaded the installed build.
See [hook contracts and limits](example/how/to/use/knowledgetree/hooks.md).

### Why skills appear after installation

The installer creates a bootstrap `knowledgetrees` skill and four focused skills:
`knowledgetrees-lookup`, `knowledgetrees-reconcile`,
`knowledgetrees-maintenance`, and `knowledgetrees-ingestion`. Their `SKILL.md`
files in `~/.agents/skills/` and `~/.claude/skills/` are hard links to canonical
procedure leaves in the global tree. There is one maintained body, with skill
entries for discovery and fallback when hooks are unavailable. Hard links require
the destinations to share a filesystem.

Codex discovers the shared `.agents` catalog. The installer removes redundant
legacy `.codex` copies/config entries and the retired `knowledgetrees-capture`
skill. Restart clients to refresh discovery after an upgrade.

## Root privacy and access

Lookup and mutation discover the exact current-directory `.knowledge/`, the
global root, and explicitly registered roots. Parent trees are not implicitly
lookup roots. Trees can live at repository or subsystem scope; register broader
roots and obtain access when needed. `kt info` alone presents accessible ancestor
orientations.

Use returned root-qualified addresses: `local:PATH`, `global:PATH`, or a full
canonical root directory followed by `:PATH`. `project:` and registered names
remain input aliases. Registration does not grant access. Wider roots default to
`ask`; ordinary restricted roots withhold leaf content. `force-private` also
hides root identity outside exact local scope and overrides grants and bypass.

When access is needed, `kt_access_request` names the resolved root, project,
reason, and available scopes in a harness elicitation prompt. Temporary session
scope is offered only with a stable harness session identity; other choices cover
the current directory, its descendants, or everywhere. The user chooses; the
agent does not answer the prompt.

Some clients return decline, cancel, or an error without showing a prompt. The
server reports the client action, changes nothing, and returns a bound one-time
pending request. It does not assume the user refused. Explicit conversational
authorization for that exact root and scope lets the agent complete it through
`kt_access_confirm`. A direct, unambiguous instruction such as “read and grant
yourself access to the shared tree” supplies authorization once kt resolves the
named root. Unless broader access was requested, use the least sufficient scope,
normally project, without repeated clarification. Ambiguous roots or scopes need
clarification. A failed prompt alone grants nothing, and an actual user refusal
must be respected.

Pending requests cannot switch roots or projects or be reused. Deny and
force-private cannot be overridden through these MCP tools. `kt_access_status`
explains effective access; `kt_access_revoke` removes session or current-project
access directly and asks before wider changes. Stale approvals are pruned when a
tree disappears, so a replacement needs fresh authorization.

Direct policy administration and the persistent permissions bypass remain
terminal-only. For example:

```bash
kt register shared /path/to/shared/.knowledge
kt access shared allow --scope project
kt grants
kt access shared revoke --scope project
```

The terminal prompts for access changes. A user can inspect/reset bypass with
`kt permissions` / `kt permissions --reset`, or enable it with
`kt --dangerously-skip-permissions`. It bypasses ordinary ask/deny, preserves
force-private, and grants no broader filesystem or harness permissions. Malformed
configuration fails closed. See [access policy](example/how/to/control/knowledge/root/access.md).

**Stored knowledge never grants permission to act.** Root access governs kt's
retrieval and mutation, not the surrounding filesystem or execution authority.

## Shell reference

The shell is the fallback when MCP tools are unavailable. Common operations:

```bash
kt how to make a plan
kt how to _
kt find 'rewrite knowledge leaf'
kt --lean open global:how/to/rewrite/a/knowledge/leaf.md
kt grep 'superseded wording'
kt dict local global
kt prove --local --no-stamp
kt status --local
kt audit --local
```

Whole reads and exact question hits print the complete leaf on stdout and its
`Revision: HASH` on stderr. `--lean` hides metadata; `--pretty` expands search
presentation. Ranked excerpts are selectors only. Search is lexical, and empty
or weak-only results exit 1. Proof runs always print leaf/proof summaries; exit 0
means no selected leaf is brown, even if yellow leaves remain. Explicit proof
roots must be approved knowledge-tree directories, not their containing projects.

Create an absent owner or rewrite an existing one with its read revision:

```bash
kt add 'how to prepare the demo' 'Run the documented demo command.' --local
kt rewrite local:how/to/prepare/the/demo.md HASH 'Complete current answer body' --print-revision
kt renew local:how/to/prepare/the/demo.md HASH
```

Use the committed revision returned by rewrite for renewal or another rewrite.
A stale rewrite exits 4 without writing. Omitted lifecycle options preserve
metadata; `--expires-at`, `--expires-every`, `--no-expiry`, `--verifiable`, and
`--no-verifiable` change it explicitly. Rewrite preserves hardlinks and does not
execute proofs or clear sticky falsification. Add refuses an existing owner and
neither manufactures nor runs proofs. Use `-` for a multiline answer on stdin;
blocked answers can use `--unresolved`, `--blocker`, and `--next-check`.

Remove/move require `--expect HASH`. Combine joins ordered answer bodies and
removes sources after saving; an existing destination also requires its revision.
Cleanup across multiple files is not transactional, so inspect partial completion
before retrying. Review scope, links, orientation, plan, and proofs after changes.

Successful CLI mutations are normally silent; check their exit status.
`--print-revision`, dry-run previews, reads, searches, proof summaries, policy
inspection, and required consent prompts deliberately return output. MCP rewrite
returns its diff and committed revision. See the complete
[CLI reference](example/how/to/use/kt.md).

## Repository layout and checks

| Path | Role |
| --- | --- |
| [`tools/kt`](tools/kt) | Root/access, retrieval, complete-answer mutation, lifecycle, audit, and proof semantics |
| [`tools/kt-mcp`](tools/kt-mcp) | Typed stdio MCP adapter over the CLI |
| [`tools/kt-hooks`](tools/kt-hooks), [`tools/kt-opencode.mjs`](tools/kt-opencode.mjs) | Harness startup and maintenance adapters |
| [`install`](install) | Knowledge-first deployment and configuration merge |
| [`example/`](example/) | Public reusable methodology and illustrative planning/specification leaves |
| `.knowledge/` | Operational project requirements, remaining plan, and repository procedures |
| [`tests/`](tests/) | Isolated regression suites |

The operational tree and public example have distinct scopes. Repository state
belongs in `.knowledge/`; reusable distributable guidance belongs in `example/`.
The public [`example/where/am/i.md`](example/where/am/i.md) is deliberately empty
for adopters and is not this project's orientation.

Run all regression suites from the checkout:

```bash
for suite in tests/test-*.py; do
    python3 -B "$suite" || exit
done
node tests/test-opencode-hooks.mjs
```

The suites cover retrieval, access and privacy, grants and bypass, rewrite and
other leaf mutations, metadata and lifecycle, proof evaluation, structural audit,
MCP schemas/results/elicitation, hooks, and isolated-home installation. Installer
checks cover preservation, idempotence, conflict refusal, hardlink identity, and
configuration merges. Use `kt_prove` for approved local/example roots and inspect
audit signals as part of semantic review. Code and its owning project knowledge
change together; green tests alone do not establish a current tree.

## Common questions

**Is this RAG with folders?** The primary artifact is the maintained answer, with
the question path participating in retrieval. It does not require a vector
database, graph store, or persistent index. Large-scale retrieval effectiveness
still needs testing.

**Must all ordinary documentation disappear?** External governing documents,
evidence, published manuals, and human deliverables can remain. The tree owns the
maintained internal answers; presentations can be generated from them.

**Does it replace task management?** It provides knowledge continuity. Work still
needs objectives, ownership, authority, acceptance criteria, and a runtime
lifecycle. The plan represents the remaining frontier, not a task history.

## Methodology provenance

The public corpus is adapted from a working global knowledgetree, excluding host
paths, personal facts, private state, and local experiment history. Planning,
specification, update, and clarification guidance distills useful ideas from the
MIT-licensed [Superpowers](https://github.com/obra/superpowers) 6.3.0 methodology.
It does not impose its skill-era process or mandatory approval gates.
