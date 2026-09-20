---
status: green
revised_at: "2026-09-20T16:23:47+10:00"
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
`status: green|yellow|brown` and timezone-aware `revised_at`. `kt check ADDRESS
HASH` alone records the manual whole-leaf `checked_at`. Optional `expires_at`
and `expires_every` describe time-based freshness; `verifiable: true` is a reviewed
assertion that eligible proofs cover every factual claim. Skill entry leaves may
also need `name` and `description` for harness discovery. Blockers, next checks,
evidence, provenance, and review conditions belong in the answer body; root and
path supply scope. All stored timestamps are ISO 8601 with a timezone. Unsupported
or malformed front matter is rejected by write commands and brown in proof checks.
Empty orientation and spine leaves created by `kt init` remain empty until filled.

`kt add` and `kt rewrite` accept answer bodies and generate front matter. Options `--expires-at TIMESTAMP` and `--expires-every DURATION` set freshness; `--verifiable` asserts complete proof coverage. Rewrite preserves omitted optional fields; `--no-expiry` and `--no-verifiable` clear them. `kt add`, `kt rewrite`, and `kt combine` set `revised_at` for changes. New
and revised answers start yellow; a brown leaf stays brown through a rewrite until
an independent whole-leaf check. `kt prove` writes the evaluated color. Elapsed
expiry makes an otherwise passing leaf yellow; it reports yellow counts without
listing their paths. Brown is sticky after proof failure or malformed structure,
prints the affected path, and causes a nonzero exit. Proof verification timestamps
belong to individual `Proof:` markers and never advance manual `checked_at`.
An unflagged brown leaf needs an independent `kt check` after repair. A reviewed
`verifiable: true` leaf requires at least one proof and becomes green when every
proof runs and passes with valid structure, even after a prior failure or expiry.
Missing or failed proofs make it brown. `--no-stamp` is read-only. Proof and status
writes preserve hardlink identity and avoid steady-state timestamp churn.

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

A behavior or policy change is complete only after a semantic consistency review
of affected code and CLI behavior against local/global owners, public example,
README, startup hook payloads and installer templates, and installed guidance.
Generated copies must be refreshed and checked for drift. Tests and `kt prove`
are necessary checks, not substitutes for reading and reconciling prose.

## Retrieval and maintenance

The CLI supports sentence-prefix questions, root-qualified `kt open`, ranked
`kt find`, `kt grep` (literal or regex text search that respects access), `kt dict`, `kt add`, `kt rewrite`, `kt check`, `kt status` (read-only listing of non-green leaves with reasons), `kt rm`, `kt mv`,
`kt combine`, root registration/access, and `kt prove`. Exact reads print verbatim
content on stdout and its SHA-256 revision on stderr. `kt rewrite ADDRESS HASH
BODY` requires the full-read revision, rejects stale writes, preserves
hardlinks and still-valid answer text, resets changed proof markers, and produces
no normal success output. Evidence belongs in the answer. `kt rm` and `kt mv`
require `--expect`; move refuses overwrites and preserves bytes. `kt combine`
concatenates source bodies in order, resets inherited proof stamps and manual
check time, keeps brown if any source was brown, and removes sources only after a
successful save. Destructive maintenance must detect conflicts and preserve
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
Agents do not approve access on the user's behalf. The root registry and
unrelated host permissions survive installation.

`kt init [ORIENTATION]` creates an empty local tree and spine without overwriting
one. `kt info` prints the canonical global procedure, exact local orientation,
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
Claude Code, Codex, OpenCode, and Copilot hooks provide startup, failure, and one-shot
capture-review reminders without storing raw logs. Hook support must respect
session boundaries and avoid self-triggering loops. The OpenCode backend must
restart to load a changed plugin; Codex hook definitions require native trust; Claude Code definitions are reviewed with `/hooks`.
Claude Code drops hook context past roughly 10,000 characters, so its startup
hook sends an instruction to run `kt info` directly when the output exceeds
9,500 bytes, rather than a silently truncated startup output.

The 16 MCP tools (`kt_info`, `kt_lookup`, `kt_find`, `kt_grep`, `kt_read`, `kt_edit`,
`kt_rewrite`, `kt_undo`, `kt_add`, `kt_dict`, `kt_roots`, `kt_prove`, `kt_status`,
`kt_access_status`, `kt_access_request`, `kt_access_revoke`) delegate every operation to the CLI so
revision, access, locking, and proof semantics are unchanged, and carry read-only and
destructive annotations. Destructive, initialization, and access-policy commands stay
CLI-only, and no input may inject a CLI option. The one exception is access approval:
`kt_access_request` asks the user through MCP elicitation and persists an accepted
`allow` with the CLI's own `apply_access_decision`. Only the user's answer grants;
denied and force-private roots are never prompted for, and the CLI itself keeps its
own-terminal confirmation. Access can be given back: `kt grants` reports each root's
effective access and its source, `kt access ROOT revoke` narrows it (terminal), and
`kt_access_revoke` does so from the harness (direct for this directory, user-confirmed
for anything wider). Approvals are path-keyed, so every run prunes project grants, everywhere-allowed registrations, and auto-named
ask registrations whose tree no longer exists; deny, force-private, and user-named ask
registrations are kept.

## Proof and release checks

Proof commands are explicit, bounded, and read-only predicates attached to
concrete assertions. `kt prove` checks every selected proof, reports aggregate
colors and brown paths, and supports exact local, global, and other accessible
root selection. The verifier does not repair prose or infer complete proof
coverage. Agents inspect claim-to-proof coverage before setting `verifiable`.
Publication checks include Python and OpenCode regressions, scoped project,
example, and installed-global proof sweeps, instruction-sync checks, installed
CLI byte comparison, a public-content audit (`how/to/audit/public/content/before/publishing.md`), and Git whitespace/working-tree
checks. User authorization to publish persists for in-scope work across turns unless changed or withdrawn; no separate release gate is imposed by this repository.
