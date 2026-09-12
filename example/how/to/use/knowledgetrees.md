---
name: knowledgetrees
description: 'Session bootstrap with mandatory observable lookup gates, semantic retrieval, proof checks, and continuous knowledge capture.'
metadata:
  verified_at: '2026-09-12T18:20:19+10:00'
  verified_by: codex /root
  scope: public knowledge-tree example and distributable skill
  source: sanitized operational recommendations and the canonical knowledge-tree contract
  verification: Reviewed extracted obligations, observable lookup gates, navigation, capture, proof semantics, and scope preservation.
  review_when: Recheck when retrieval gates, bootstrap, or knowledge-tree procedures change.
---

Knowledge trees are the authoritative semantic answer substrate; context is working
memory. Bootstrap once at the start of a fresh agent session, before substantive
work. Continue the loaded procedure across turns and tasks; rebootstrap only after
a new session or genuine loss of the procedure.

## Bootstrap

1. Establish the nearest applicable project root and `~/.knowledge`, with `how/`,
   `what/`, `where/`, `why/`, and a truthful `where/am/i.md`. Create missing
   repository spine leaves: `what/is/the/{spec,plan,state}.md` and `what/is/next.md`.
2. Run `~/.knowledge/.tools/verify-knowledgetree-proofs --root ROOT` for each active
   root. Stop on falsification; inspect and repair evidence within current authority.
3. Read nearest and global `where/am/i.md`, then the active repository's four spine
   leaves. Each orientation must explain every canonical branch and give actual
   exemplar paths; repair missing routes from evidence, not invented filenames.
4. Entering another directory scope requires orientation and verification there,
   not another skill invocation. Detailed root and spine rules live in maintenance.

## Observable lookup gates — consult the tree BEFORE the shell

- A probe returned not-found, permission-denied, missing package, or unexpected version.
- About to install something, escalate privileges, or modify host state.
- About to use an environment-specific path, tool, or device node.
- About to write outside the repository.
- The "obvious" answer comes from training data but is host- or project-specific.

A failed probe is a retrieval event, not an error to work around. These gates remain
active after bootstrap; stored knowledge never grants permission to perform an action.

## Operating loop and direct-answer routes

Lookup -> discover -> verify -> record -> use. Gate plus tree hit: use the checked
answer; no duplicate capture. Gate plus miss: capture the verified reusable answer
before continuing, or record `status: unresolved` with blocker and next check.
Resolve these paths from the installed global knowledge root, not the harness's
`SKILL.md` directory; local orientation routes select project-specific answers.
The installer also advertises these four procedures as focused skills hardlinked
to their canonical leaves. Use them when their triggers apply; this is not another bootstrap.

- Lookup: `how/should/an/agent/traverse/a/knowledge/tree.md` — read before gated descent.
- Capture: `how/to/add/knowledge/leaves.md` — read before creating or changing knowledge.
- Maintenance: `how/to/maintain/a/knowledge/tree.md` — read before proof reliance, repairs, or task completion.
- Ingestion: `how/should/legacy/documents/be/ingested/into/a/knowledge/tree.md` — read before corpus migration.

Continuously capture reusable discoveries, keep paths sentence-derived and free of
underscores, and update repository state and next-action leaves before completion.
Project facts stay in their scope; private or restricted knowledge stays out of
public and global exports. Current higher-authority instructions always govern.
