---
name: knowledgetrees
description: 'Bootstrap once per fresh session; use kt first for new questions, resolve lookup misses, check proofs, and capture missing knowledge before continuing.'
metadata:
  verified_at: '2026-09-12T20:29:52+10:00'
  verified_by: codex /root
  scope: public knowledge-tree example and distributable skill
  source: sanitized operational recommendations and the canonical knowledge-tree contract
  verification: Reviewed kt-first lookup, mandatory miss classification, capture timing, retained root/proof/scope obligations, and installed hardlink identity.
  review_when: Recheck when retrieval gates, bootstrap, or knowledge-tree procedures change.
---

Knowledge trees are the authoritative semantic answer substrate; context is working
memory. Bootstrap once at the start of a fresh agent session, before substantive
work. Continue the loaded procedure across turns and tasks; rebootstrap only after
a new session or genuine loss of the procedure.

## Bootstrap

Use `kt` from PATH, or `~/.knowledge/.tools/kt` if PATH has not been configured.
`kt roots` shows current roots; its preview does not replace full orientation reads.

1. Establish the nearest applicable project root and `~/.knowledge`, with `how/`,
   `what/`, `where/`, `why/`, and a truthful `where/am/i.md`. Create missing
   repository spine leaves: `what/is/the/{spec,plan,state}.md` and `what/is/next.md`.
2. Run `kt proof --root ROOT` for each active
   root. Stop on falsification; inspect and repair evidence within current authority.
3. Read nearest and global `where/am/i.md`, then the active repository's four spine
   leaves. Each orientation must explain every canonical branch and give actual
   exemplar paths; repair missing routes from evidence, not invented filenames.
4. Entering another directory scope requires orientation and verification there,
   not another skill invocation. Detailed root and spine rules live in maintenance.

## Default action: new question -> kt first

For a new question not already answered by adequately checked loaded knowledge,
the first lookup action is a question-prefix call such as `kt where is vivado`
or `kt how to make a plan`, or `kt open` for a known leaf path. Use `kt find`
for deliberately broad keyword searches. Read listed matches with `kt open project:PATH`
or `kt open global:PATH`; check evidence and relevant proofs before reliance.
Do not start with external grep, host probes, or training-data assumptions.

Question conventions: `where/is/` for locations, `how/to/` for procedures,
`when/to/` for decision triggers, `what/is/` for definitions/current state,
and `why/does/` or `why/is/` for rationale. Longer sentence prefixes also work.
kt walks matching words into directories; at the first mismatch it ranks the
remaining words only inside that branch. Weak keyword coverage widens one parent
at a time; exact leaf hits return full content. `kt how to _` lists that branch.

Failure to find information via `kt` means you MUST determine whether a leaf
exists: retry useful keywords/synonyms, then inspect plausible semantic paths in
the applicable roots. A search miss is not proof of absence. If a leaf exists,
read it and correct stale or incomplete knowledge as needed; do not duplicate it.
If no leaf exists, investigate within authority and add the appropriately scoped
leaf. If unresolved, add `status: unresolved` with blocker and next check.
Once an answer is established, capture it before the next unrelated tool call
or completion. Verification and capture calls are part of resolving the question.

## Operating loop and direct-answer routes

Lookup -> establish leaf existence -> discover -> verify -> record -> use.
A checked hit needs no duplicate capture; a missing answer creates a capture
obligation, not permission to move on. Failed probes are new lookup events, not
errors to work around. Stored knowledge never grants execution authority.
Resolve these paths from the installed global knowledge root, not the harness's
`SKILL.md` directory; local orientation routes select project-specific answers.
The installer also advertises these four procedures as focused skills hardlinked
to their canonical leaves. Use them when their triggers apply; this is not another bootstrap.

- Lookup: `how/should/an/agent/traverse/a/knowledge/tree.md` — kt-first lookup and miss resolution.
- Capture: `how/to/add/knowledge/leaves.md` — read before creating or changing knowledge.
- Maintenance: `how/to/maintain/a/knowledge/tree.md` — read before proof reliance, repairs, or task completion.
- Ingestion: `how/should/legacy/documents/be/ingested/into/a/knowledge/tree.md` — read before corpus migration.

Continuously capture reusable discoveries, keep paths sentence-derived and free of
underscores, and update repository state and next-action leaves before completion.
Project facts stay in their scope; private or restricted knowledge stays out of
public and global exports. Current higher-authority instructions always govern.
