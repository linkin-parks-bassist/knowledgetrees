---
status: green
revised_at: "2026-09-24T10:31:58+10:00"
---

The public repository contains the readable README, a self-contained `tools/kt`
CLI, the harness adapters (`tools/kt-hooks`, `tools/kt-opencode.mjs`, and the
`tools/kt-mcp` MCP server), the `install` script, tests, this operational `.knowledge/` tree, and the
public `example/` corpus. The example is distributable guidance with an empty
`where/am/i.md`; repository-specific state stays here. Public leaves must not
contain private host, customer, or owner-identifying material. The repository
remains connected to its intended GitHub remote; publication follows the owner's current instructions, including earlier in-scope authorization.

## Leaf format and lifecycle

Nonempty leaves use flat Markdown front matter. Automated fields are
`status: green|yellow|brown` and timezone-aware `revised_at`. `kt renew ADDRESS
HASH` alone records the manual whole-leaf `checked_at` (then it re-runs that leaf's own proofs and leaves the leaf green or brown). Optional `expires_at`
and `expires_every` describe time-based freshness; `verifiable: true` is a reviewed
assertion that eligible proofs cover every factual claim. Skill entry leaves may
also need `name` and `description` for harness discovery. Blockers, next checks,
evidence, provenance, and review conditions belong in the answer body; root and
path supply scope. All stored timestamps are ISO 8601 with a timezone. Unsupported
or malformed front matter is rejected by write commands and brown in proof checks.
The empty orientation created by neutral `kt init` remains empty until filled; only `kt init --project` creates empty spec, plan, state, and next placeholders. A leaf is a current answer, never a chronological log: task narration, session notes, progress updates, and tool transcripts are tree poisoning and must not be appended. History remains only when it explains a current constraint or decision; Git or an external log owns chronology.

`kt add` and `kt rewrite` accept answer bodies and generate front matter. Options `--expires-at TIMESTAMP` and `--expires-every DURATION` set freshness; `--verifiable` asserts complete proof coverage. Rewrite preserves omitted optional fields; `--no-expiry` and `--no-verifiable` clear them. `kt add`, `kt rewrite`, and `kt combine` set `revised_at` for changes. A new leaf starts green (with `checked_at` too when `--expires-every` is given), and a rewrite keeps the status and `checked_at`, so a brown leaf stays brown through a rewrite until
an independent whole-leaf check. `kt combine` yields the worst status of its sources. `kt prove` writes the evaluated color and only ever lowers it; the sole leaf it raises is a `verifiable: true` one whose proofs all pass. Elapsed
expiry makes an otherwise passing leaf yellow; it reports yellow counts without
listing their paths. Brown is sticky after proof failure or malformed structure,
prints the affected path, and causes a nonzero exit. Every executable predicate follows
an exact, timeless `Proof:` delimiter; proof runs never write an outcome or timestamp
to that marker and never advance manual `checked_at`. A writing proof run accepts
legacy `(verified|falsified at …)` markers as migration input and silently normalizes
them to `Proof:` without parsing the timestamp; `--no-stamp` accepts them read-only. An unflagged brown leaf needs
an independent `kt renew` after repair. A reviewed
`verifiable: true` leaf requires at least one proof and becomes green when every
proof runs and passes with valid structure, even after a prior failure or expiry.
Missing or failed proofs make it brown. `--no-stamp` is fully read-only; ordinary
proof runs may write only leaf lifecycle status. Status writes preserve hardlink
identity, while stable results avoid steady-state file churn.

A zero-exit `kt prove` run means only that selected leaves had no brown-level
failure detected at that time; yellow expiry warnings may remain. Green includes
proof-free leaves. Even `verifiable: true` relies on the reviewed coverage
assertion and predicates that genuinely test their claims.

## Current-truth priority

Known stale or contradictory active knowledge is an immediate repair obligation,
even when status is green. Agents stop relying on it, check current evidence,
rewrite the owner while preserving valid content, and correct affected leaves and
guidance before unrelated work or completion. If truth remains unresolved, remove
the unsupported claim and record the blocker and next check. Passing proofs and
metadata colors do not establish correctness of unproved prose.

A brown leaf or failed proof check is a priority-one incident and mandatory stop
condition, including during startup when the user gave no task. Before any other
action, the agent's first response prominently reports the brown result and leaf;
a neutral readiness response is noncompliant. The agent then limits work to finding
why the leaf or proof differs from reality, choosing and performing the safest
remediation (normally correcting its content or proof), independently reviewing it,
and re-checking until brown clears. If safe remediation cannot be established, the
agent asks the user for guidance. Only explicit user permission to ignore that
specific brown status allows unrelated work to resume, without validating the leaf.

A behavior or policy change is complete only after an explicit affected-owner inventory covers narrow and central procedures, policy/access guidance, local/global owners, public example, README and CLI help, startup and installer surfaces, repository spine leaves, and installed guidance. Search positively for the new behavior and negatively for superseded counts, lists, fallbacks, and limitations; read every hit in context and repeat the negative searches after repair. Generated copies must be refreshed and checked for drift. Tests, `kt prove`, timestamps, and byte equality are necessary checks, not substitutes for reading and reconciling every affected owner.

## Retrieval and maintenance

The CLI supports sentence-prefix questions, root-qualified `kt open`, ranked
`kt find`, `kt grep` (literal or regex text search that respects access), `kt dict`, `kt add`, `kt rewrite`, `kt renew`, `kt status` (read-only listing of non-green leaves with reasons), `kt rm`, `kt mv`,
`kt combine`, root registration/access, and `kt prove`. Exact reads print complete content on stdout, adding a presentation-only trailing
newline when stored bytes lack one, and print the stored bytes' SHA-256 revision on
stderr. Every non-empty CLI stdout or stderr stream ends with a newline. `kt rewrite ADDRESS HASH
BODY` requires the full-read revision, rejects stale writes, preserves
hardlinks and still-valid answer text, leaves exact `Proof:` markers as supplied in
the answer, and produces no normal success output. Evidence belongs in the answer. `kt rm` and `kt mv`
require `--expect`; move refuses overwrites and preserves bytes. `kt combine`
concatenates source bodies in order, preserves exact, timeless `Proof:` markers,
resets manual check time, keeps brown if any source was brown, and removes sources
only after a successful save. Destructive maintenance must detect conflicts and preserve
changed sources. All mutations honor root access and forced privacy.

Default lookup output is compact plain text with root-qualified addresses,
coverage scores, excerpts, and status. `--pretty` supplies a human-oriented view.
Empty or weak search results exit nonzero without treating a miss as proof of
absence. `does/` and `is/` answer yes/no questions directly. `kt dict` emits
sorted, unique, useful final path segments from accessible trees without reading
bodies or exposing restricted paths. Knowledge belongs at every scale, including
function contracts, code details, architecture, decisions, specs, and plans.

## Roots, startup, and installation

The exact current-directory `.knowledge/` tree and explicit registered roots are
used; kt never discovers parent trees automatically. Wider roots default to ask.
A user-confirmed persistent permission bypass may skip ordinary ask/deny rules,
but force-private always wins outside the exact local tree. Protected subtrees
must not leak through lookup, reads, capture, symlinks, proofs, or startup.
Agents never invent approval. Normal grants use MCP elicitation; if a client cannot complete it, explicit conversational authorization for the pending request's exact root and scope permits `kt_access_confirm`. Wider revocation uses an equivalent one-time repeat-call continuation. Direct policy administration remains terminal-only. The root registry and
unrelated host permissions survive installation.

`kt init [ORIENTATION]` creates a neutral local tree with the six canonical
branches and `where/am/i.md`, registers it under `ask` without cross-project
access, and refuses to overwrite an existing tree. `kt init --project
[ORIENTATION]` additionally creates empty spec, plan, state, and next leaves. `kt info` prints the canonical global procedure, exact local orientation,
accessible dictionary, and local proof result in that order; without a local
tree or local orientation it falls back to the global orientation and proof. Startup hooks inject
its complete output through the final proof summary. The bootstrap is once per
fresh session, then kt-first retrieval and miss resolution apply throughout the
session. The example and global instructions include lookup, capture, maintenance,
ingestion, and proof guidance. An encountered miss is resolved to an existing
owner or an investigated new or unresolved answer before unrelated work resumes.

The installer merges the public example guidance into `~/.knowledge` without
installing the example spine, preserves existing orientation, installs the CLI,
hooks, and MCP server (registered with all four harnesses; `--no-mcp` skips it), removes its obsolete home AGENTS bootstrap, and hardlinks skill entry points to the
canonical installed procedure leaves. It preserves unrelated configuration.
OpenCode permission changes require informed `[n/Y]` consent before writes.
Claude Code, Codex, OpenCode, and Copilot integrations provide startup context only. The installer removes its formerly managed non-startup reminder hooks while preserving unrelated hooks; no managed prompt, tool-result, failure, stop, idle, call-counter, or capture-review hook remains active. The OpenCode backend must
restart to load a changed plugin; Codex hook definitions require native trust; Claude Code definitions are reviewed with `/hooks`.
Claude Code drops hook context past roughly 10,000 characters, so its startup
hook sends an instruction to call the `kt_info` tool (or run `kt info`) when the output exceeds
9,500 bytes, rather than a silently truncated startup output.

The 23 MCP tools (`kt_info`, `kt_lookup`, `kt_find`, `kt_grep`, `kt_read`, `kt_rewrite`, `kt_edit`, `kt_undo`, `kt_add`, `kt_rm`, `kt_mv`, `kt_combine`, `kt_init`, `kt_renew`, `kt_dict`, `kt_roots`, `kt_register`, `kt_prove`, `kt_status`, `kt_access_status`, `kt_access_request`, `kt_access_confirm`, `kt_access_revoke`) delegate every operation to the CLI so revision, access, locking, and proof semantics are unchanged, and carry read-only and destructive annotations. Whole-leaf reads and exact lookup hits return the complete answer plus its SHA-256 `Revision:` line and no other metadata; neither MCP nor kt supports partial leaf reads. Ranked excerpts are selectors, not reads. `kt_rewrite` is the standard editing tool and requires that read hash; the CLI rejects stale hashes under lock. `kt_edit` is used only for economy on a tiny surgical exact-match change, and renewal still requires the server's remembered whole read. Agent guidance names the tools first with the shell only as the fallback. `kt_add`, `kt_prove`, and `kt_status` accept an approved root label or absolute root path as an alternative to local/global scope. `kt_rm` and `kt_mv` require a whole-read source hash; `kt_combine` requires hashes for every source and any existing destination. `kt_init` creates the neutral baseline by default, accepts `project: true` for the four project-spine placeholders, automatically registers the new tree under `ask`, and retains the CLI refusal to overwrite an existing tree; `kt_register` records an existing root under `ask` without granting it. Direct access-policy mutation and the permissions bypass stay CLI-only, and no input may inject a CLI option. The one exception is access approval:
`kt_access_request` sends MCP elicitation and persists `allow` with the CLI's own
`apply_access_decision` only for an accepted response with a valid scope. Denied
and force-private roots are never prompted for, and the CLI itself keeps its
interactive confirmation. An unexplained client decline, cancellation, invalid response, error, or lack of elicitation capability is not attributed to the user and grants nothing. The tool returns a one-time pending request without suppressing a later attempt. Explicit user authorization in conversation for its exact root and scope permits `kt_access_confirm`; unknown, reused, mismatched, denied, and force-private requests fail. Wider revocation has the same exact-request continuation and neither path authorizes a permissions bypass. Access can be given back: `kt grants` reports each root's
effective access and its source, `kt access ROOT revoke` narrows it (terminal), and
`kt_access_revoke` does so from the harness (direct for this directory, user-confirmed
for anything wider). Approvals are path-keyed, so every run prunes project grants, everywhere-allowed registrations, and auto-named
ask registrations whose tree no longer exists; deny, force-private, and user-named ask
registrations are kept.

## Proof and release checks

Proof commands are explicit, bounded, and read-only predicates attached to
concrete assertions. `kt prove` checks every selected proof, prints aligned `Leaves:` and `Proofs:` count lines with `SUCCESS` or `FAIL`, reports brown paths, and supports exact local, global, and other accessible root selection. The verifier does not repair prose or infer complete proof
coverage. Agents inspect claim-to-proof coverage before setting `verifiable`.
Publication checks include Python and OpenCode regressions, scoped project,
example, and installed-global proof sweeps, instruction-sync checks, installed
CLI byte comparison, a public-content audit (`how/to/audit/public/content/before/publishing.md`), and Git whitespace/working-tree
checks. User authorization to publish persists for in-scope work across turns unless changed or withdrawn; no separate release gate is imposed by this repository.
