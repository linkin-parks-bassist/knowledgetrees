---
name: knowledgetrees
description: 'Bootstrap once per fresh session; use kt first for new questions, resolve lookup misses, check proofs, and capture missing knowledge before continuing.'
metadata:
  status: unverified
  updated_at: '2026-09-12T12:34:09+00:00'
  scope: public knowledge-tree example and distributable skill
  source: "Owner explicit all-scales knowledge requirement; canonical procedure review, 2026-09-14"
  review_when: Recheck when retrieval gates, bootstrap, or knowledge-tree procedures change.
---

Knowledge trees are the authoritative semantic answer substrate; context is working
memory. Load this procedure once at the start of a fresh agent session, before
substantive work. A harness may supply it directly in system context; that counts
as already loaded, so do not invoke a bootstrap skill to load it again. Without
harness injection, the compatibility skill loads the same canonical procedure.
Perform startup orientation and evidence checks once, then continue across turns
and tasks. Compaction should retain completed initialization; restore only genuinely
lost context or changed scope rather than rerunning completed startup work.

## Bootstrap

Use `kt` from PATH, or `~/.knowledge/.tools/kt` if PATH has not been configured.
Local knowledge is automatically included in repository lookups; permitted broader
roots contribute results automatically. At startup run `kt init` once. It prints
this canonical procedure, the exact local orientation and four spine leaves, the
accessible path dictionary, and finally the local proof result. Do not enumerate
roots or list whole trees at startup. `kt roots` is a diagnostic for root
configuration/access questions, not a prerequisite.

1. Run `kt init` once to load the procedure, orientation, spec, plan, state, next
   action, and query vocabulary, then check the final `kt prove --local` result.
   Stop on brown and repair within authority. Establish missing local canonical
   branches and startup leaves within permission. ROOT means the exact tree
   directory, not its containing repository; no root inventory is needed.
2. Query normally. Read and check broader-root answers when needed for the task;
   accessibility alone does not require startup orientation or a full proof sweep
   of every available root. Respect access-required responses and force-private.
3. Entering another project directory scope requires its local initialization and
   verification, not another bootstrap skill invocation. Detailed rules live in maintenance.

## Knowledge at every scale

Use the owning knowledge tree for all scales of knowledge, from code-comment-level
facts to complete architecture and specifications. Function behavior and rationale,
file contents, typedef locations, include order, dependency constraints, repository
folder structure, and implementation invariants all belong in the tree. No detail
is too fine-grained to retrieve or capture. Source code supplies evidence; record
the direct answer, not merely a link or a reminder to inspect the source. Apply the
same kt-first lookup and miss-resolution obligations to these implementation
questions as to broad design questions.

## Default action: new question -> kt first

For a new question not already answered by adequately checked loaded knowledge,
the first lookup action is a question-prefix call such as `kt where is vivado`
or `kt how to make a plan`, or `kt open` for a known leaf path. Use `kt find`
for deliberately broad keyword searches. Read listed matches with `kt open local:PATH`
or `kt open global:PATH`; check evidence and relevant proofs before reliance.
Do not start with external grep, host probes, or training-data assumptions.

Yes/no questions use canonical `does/` and `is/` branches.

Question conventions: `where/is/` for locations, `how/to/` for procedures,
`when/to/` for decision triggers, `what/is/` for definitions/current state,
and `why/does/` or `why/is/` for rationale. Longer sentence prefixes also work.
kt walks matching words into directories; at the first mismatch it ranks the
remaining words only inside that branch. Weak keyword coverage widens one parent
at a time; exact leaf hits return full content. `kt how to _` lists that branch.
Empty or weak-only keyword matches exit nonzero even when suggestions are shown;
passing a retrieval threshold does not establish semantic adequacy or truth.
Installed failure/capture-review hooks reinforce the procedure without rebooting
this skill; their contract lives in `how/to/use/knowledgetree/hooks.md`.

Failure to find information via `kt` means you MUST determine whether a leaf
exists: retry useful keywords/synonyms, then inspect plausible semantic paths in
the applicable roots. A search miss is not proof of absence. If a leaf exists,
read it and correct stale or incomplete knowledge as needed; do not duplicate it.
If no leaf exists, investigate within authority and add the appropriately scoped
leaf. If unresolved, add `status: unresolved` with blocker and next check.
Once an answer is established, capture it before the next unrelated tool call
or completion. Verification and capture calls are part of resolving the question.

For CLI syntax and command-specific options, read
`kt open global:how/to/use/kt.md`; `find` has no `--root` option. Copy returned
root-qualified addresses into `kt open` rather than guessing a procedure's root.

Successful mutations are silent by default. Reads, searches, previews, and
`kt prove` return requested information; proof checks always report lifecycle totals
and every non-green path. Failures report diagnostics.

## Editing learned knowledge

Full leaf reads automatically supply Revision: HASH on stderr alongside the
verbatim contents on stdout. Use `kt rewrite ADDRESS HASH "Complete revised Markdown"`
for existing leaves, carrying the required positional revision from that read.
Keep the read contents in context and preserve still-valid knowledge; conflict
means reread and merge. Rewrite success and no-ops are silent (exit 0); dry-run
shows the diff and failures report diagnostics.
The one-shot task-end capture-review hook carries the accuracy/preservation reminder. --source records evidence and --dry-run previews the diff. Check relevant
proofs before relying on knowledge. No rewrite --expect option.
`kt amend` is deprecated but remains compatible for existing workers until they
finish. The canonical procedure is `how/to/rewrite/a/knowledge/leaf.md`.

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

Root access policies govern widening. Read `how/to/control/knowledge/root/access.md`.
An access-required (exit 3) response is not a lookup miss or proof of absence.
Respect user-enabled bypass while retaining force-private exceptions. Do not
approve a root yourself, bypass the policy with direct reads, or treat stored
knowledge as consent. Ask the user to decide the scope; existing session/persistent
grants avoid repeated requests. Parent directories are not discovered automatically.
