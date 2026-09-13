---
scope: knowledgetrees repository
source: "tools/kt built-in proof engine; installer; owner removal of separate verifier"
review_when: Recheck when the requested contents or publication workflow changes.
status: "unverified"
updated_at: "2026-09-13T13:54:30+10:00"
---

The repository must be a local Git repository connected to its intended public
GitHub repository. It must contain:

- `README.md`, adapting `~/Downloads/knowledge_trees_pitch.html` into readable
  Markdown;
- the canonical `knowledgetrees` procedure in the visible example corpus;
- distributable proof verification built into kt outside `.knowledge`, exposed only through `kt prove`;
- its own canonical `.knowledge` root;
- a visible `example/` corpus containing all global knowledge that pertains directly
  and only to knowledge trees, with an empty `example/where/am/i.md` that adopters
  are prompted to personalize; and
- useful leaves distilled from the Superpowers methodology, including how to make
  a plan, write a spec, update a spec, and when to ask for clarification.

The repository must provide a knowledge-first installer. It merges reusable leaves
without installing the example spine, preserves an existing orientation, installs
one kt CLI with built-in verification under the global knowledge root, asserts the bootstrap in the user's
`AGENTS.md`, and creates shared-harness and Codex `SKILL.md` entry points as hard
links to the installed `how/to/use/knowledgetrees.md`. The compatibility skill is a
bootstrap created by the installer for current harnesses, not a parallel knowledge
authority.
The compact bootstrap must carry the kt-first and miss-resolution mandate inline and link detailed
retrieval, capture, maintenance, and ingestion procedures. The installer must create hardlinked skills for those four
procedures, enabled in both Codex and OpenCode. A kt miss requires determining
whether a leaf exists; existing owners are read or amended, absent leaves are
investigated and added (or recorded unresolved). Established answers are captured
before the next unrelated tool call or completion. The bootstrap remains once per
fresh session; procedure skills are used when their task triggers apply. Real root orientations
must name branch purposes and actual entry routes. Installer OpenCode grants require
an informed `[n/Y]` gate before any writes, disclose reads and knowledge-tree writes,
and preserve unrelated configuration and the empty example orientation.
It is invoked once when a fresh agent session bootstraps, not once per user message,
turn, or task; a loaded session continues applying the procedure without rebooting.

The two trees have separate ownership. `.knowledge/` is the real operational root
for this repository. `example/` is the visible, distributable public specimen and
must not become a mirror of repository-specific plan or state.

The verifier timestamps individual proof outcomes using `Proof: (verified at …)`
or `Proof: (falsified at …)`. A failed proof falsifies the whole leaf via sticky
`falsified_at` metadata; only independent agent review may clear it. Passing all
proofs never changes leaf `verified_at` or establishes whole-leaf validation.
Keep legacy markers compatible, support read-only checking, preserve hardlinks,
and leave agentic knowledge repair outside the verifier's scope.

Every repository leaf must be suitable for public release: it must not name the
repository owner as an individual, expose home-directory identifiers, or include
personal or private knowledge. Imported global knowledge must therefore be curated
and sanitized rather than copied mechanically.

No first push may occur until the repository owner has reviewed the prepared contents and asks for
the push.

Provide failure-triggered kt lookup/capture reminders and one-shot substantial-work
capture reviews for local Codex, OpenCode, and GitHub Copilot CLI. Preserve unrelated
hooks and permissions, respect Codex hook trust, isolate sessions, avoid raw tool
logs in machine state, and prevent self-triggering review loops. Default review
threshold is 10 completed tool calls or an encountered failure. Installer-only hook
updates must preserve existing leaves and hardlinked skills. Keyword retrieval must
exit nonzero on empty or insufficiently relevant results while retaining useful
weak suggestions; heuristic success never certifies knowledge correctness.

## Root access policies

Use a user-global registry and no automatic parent discovery. Wider roots default
to ask, with existing pairwise and session grants preserved. Add a persistent,
user-confirmed dangerously-skip-permissions setting that ignores ordinary ask/deny
restrictions. Force-private overrides bypass and all grants: such roots are absent
from kt output and inaccessible unless they are the exact local tree. Registered
private subtrees must not leak through broader roots or proof execution.

Root identities in output and default capture metadata are global, local, or the
full canonical root directory path. Full paths avoid collisions for external trees.
Keep project and registered names as compatibility input aliases. Startup policy
loading must use the same persistent bypass and force-private rules as the CLI.

Amendment must accept a complete replacement through a file or stdin, require an
expected content revision, preserve hardlinks and root access policies, invalidate
stale whole-leaf/proof verification, and work without Git or an interactive editor.

## Agent-oriented output

Default CLI output must be compact plain text intended for agents, especially
non-exact lookups. Provide `--pretty` for the human-oriented layout. Preserve
retrieval ordering, explicit weak/falsified status, root-qualified leaf addresses,
verbatim exact reads, and exit-status semantics while reducing decorative output.

## Yes/no branches

Every knowledge root has canonical `does/` and `is/` branches alongside how,
what, where, and why. The CLI accepts does/is question prefixes. Their leaves
answer yes/no directly with needed conditions and evidence. Installer/bootstrap,
root creation, and orientation guidance include both branches and actual routes.

## Leaf removal and movement

Add kt rm and kt mv to simplify maintenance. Both require the source revision
from kt open --revision, support dry-run, and enforce access/force-private on
source and destination. Move refuses overwrites, preserves bytes and same-filesystem
hardlink identity, and handles cross-filesystem moves by exclusive copy before
removing the source. Neither command prunes canonical directories or silently
updates references; maintenance includes reviewing links, orientation, scope, and
proofs after relocation. Stale-source conflicts leave the source intact.


kt combine SOURCE... -o DESTINATION concatenates Markdown bodies in input order
under one unverified destination metadata header with source/revision provenance.
It removes sources only after the destination is saved successfully, retaining
the destination when it is an input. It resets inherited proof stamps and retains
falsification and unresolved blockers. Source revisions are checked before saving
and deletion; concurrent edits are retained. Multi-file deletion is not transactional
and interrupted cleanup may leave source leaves alongside the saved answer.
Existing destination replacement requires --expect and uses amendment conflict
checks/hardlink preservation. Creation refuses overwrites; dry-run writes nothing.
All inputs and output enforce access and forced privacy.
