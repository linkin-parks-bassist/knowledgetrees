---
status: "unverified"
scope: knowledgetrees repository
source: "Authorized Projects parent-folder relocation and focused verification 2026-09-14"
review_when: Update after material repository changes.
updated_at: "2026-09-14T23:12:16+10:00"
---

The public repository's operational root is .knowledge/. The visible example/
corpus is distributable methodology and deliberately keeps where/am/i.md empty.
Project spec/plan/state must not be copied into example/. The owner published
this repository and authorizes publication of this session's CLI improvements.

## CLI and access

kt is a dependency-free, self-contained Python CLI. It handles sentence-prefix
lookup, ranked keyword search, verbatim reads, capture, revision-checked amendment,
leaf removal/movement/coalescing, root registration/access, and built-in proofs.
Default lookup output is compact plain text; --pretty opts into the human layout.
Exact questions/open stay verbatim. Lexical coverage is not semantic confidence.

Output identities/default capture scope are local, global, or canonical root path.
Project and registered names remain input aliases. Root discovery never walks
parents. Ordinary ask/deny/grant policies persist. A user-confirmed persistent
--dangerously-skip-permissions setting bypasses ordinary restrictions; force-private
wins over bypass/grants and makes roots invisible/inaccessible outside exact local
scope. Protected registered subtrees are guarded during lookup, absolute/qualified
reads, symlinks, capture, amendment, maintenance, proofs, and startup. No bypass
setting has been enabled by the agent.

rm/mv require --expect revisions and support dry-run. mv refuses overwrites,
preserves same-filesystem hardlinks, and copies exclusively across filesystems.
combine concatenates ordered Markdown bodies under one header and removes sources
after a successful save; an input destination is retained. Existing destination
replacement requires its revision. Provenance, falsification, and unresolved
blockers survive; inherited verification is reset. Conflicts retain changed
sources. Multi-file cleanup is nontransactional and partial cleanup needs inspection.

## Structure and performance

Shared root ownership/address helpers serve lookup and mutation. LeafSnapshot and
check_leaf_snapshot centralize revision/inode checks. The CLI schema is separate
from handler dispatch; the built-in proof engine is a contiguous section. Verification is exposed only through kt prove and respects force-private.

Lookup uses an invocation-only access view and lazy leaf-text reuse. No persistent
index/cache or LLM is introduced. A profiled absent question improved from about
3.02 seconds to 0.58 seconds here; an unprofiled updated run took about 0.18 seconds.
Absolute performance depends on tree size and machine. New invocations reload
policy and content, and private roots are never indexed.

## Canonical knowledge and installation

Canonical branches include how, what, where, why, does, and is; when is optional.
Does/is question prefixes return direct yes/no answers. Installer and orientation
procedures include both branches and exemplar leaves. Installation merges curated
knowledge, preserves personal orientation and registry, and hardlinks procedure
skills across harnesses. Hooks-only updates preserve customized leaves/skills.

The proof engine stamps per-proof outcomes, retains sticky whole-leaf falsification,
checks payload structure, supports read-only sweeps, and preserves hardlinks.
Passing marked predicates never verifies an entire leaf.

## Hooks and remaining uncertainty

Codex/OpenCode share bootstrap, diagnostic failure reminders, and one-shot stop/idle
capture review. Codex requires native hook trust; OpenCode must restart its backend
to load plugins, then existing sessions can resume. Historical calls are not replayed.
Force-private global procedure injection is suppressed outside exact local scope.

A commit/push boundary is detectable with tool-before APIs, but a nonblocking
reminder cannot guarantee model review before an already-issued command. Codex
supports PreToolUse context; OpenCode does not document a context return field
there. A guaranteed pre-command review needs call rejection and an agent retry.
That API limit is documented; no boundary blocker or command rewriting is installed.
Diagnostic heuristics can miss silent failures and misread diagnostic examples.
Live model compliance/resume behavior remains less established than protocol tests.

Regression suites cover CLI, access, bypass/privacy identities, amendment,
maintenance/coalescing, installer, shared hooks, OpenCode adapter, and the built-in proof engine. All suites passed after the refactor. Read-only proof sweeps passed
for the project, installed global root, and public example. The CLI and shared hook handler are deployed with identical source bytes; the
access registry was unchanged. The owner-authorized implementation update was committed and pushed to main
as 8e7a24b. A native rewrite remains a possible future optimization, contingent
on larger-corpus and warm/cold timing measurements.

Final local installation audit: PATH launcher resolves to the installed kt; kt
and the handler match repository bytes and are executable.
OpenCode plugin bytes and every managed Codex/Copilot hook definition match the
installer output. The five procedure leaves retain both harness skill hardlinks;
canonical branches and the home AGENTS bootstrap are present. Persistent bypass
is disabled. This verifies on-disk installation, not whether an existing OpenCode
backend has reloaded its plugin or a model will comply. The final knowledge audit
corrected proof-command guidance, startup privacy wording, and installed skill scope
labels; changed leaves remain unverified pending independent whole-leaf review.

Proof verification is now exposed only by kt prove. Installer code deploys only
kt and its hook handler, then checks installed knowledge through kt prove. Tests
and active documentation use that command. All regression suites passed. Project and installed-global proof sweeps passed
through kt prove; the full public specimen passed in an isolated local fixture
without saving a root grant. Local deployment matches source, both known local
copies of the separate script are removed, and the old Bash lookup prototype
delegates its proof call to kt prove. Active source/documentation references are
removed; registry bytes were unchanged.

## Interface documentation repair

The recent agent interface audit found unsupported find --root calls, incorrect
prove root selection, and guessed local addresses for global procedures. The
installed executable matched repository source before repair. The usage leaf now
has a command/address quick reference; bootstrap links it and distinguishes an
exact tree root from a repository directory. CLI help names local addresses and
explains that find searches permitted active roots without --root. Installed usage,
bootstrap and executable were updated in place; bootstrap skill hardlinks remain
shared. No project-specific transcript or private project contents were exported.

## Manual instruction refresh

The installed core kt instruction leaves are independent copies of public example
sources again; only installed canonical leaves and harness skills share hardlinks.
The local sync-kt-instructions.py is untracked and excluded through .git/info/exclude.
Run it manually to force-refresh fourteen curated instruction leaves and ten skill
paths from repository guidance, with previous revisions backed up outside the tree.
--check detects drift. Personal knowledge and project spines remain separate, and
executable/hook deployment still uses the installer. The local procedure owner is
how/to/update/installed/kt/instructions.md.

## All-scales knowledge coverage

The public definition, bootstrap, lookup, capture, maintenance, ingestion and
atomicity guidance explicitly require fine-grained implementation knowledge as
well as architecture and specs. README includes the same scope with concrete
examples. The manual refresh script now manages fourteen instruction leaves,
including the definition and atomicity guidance, and installed copies were refreshed.
Changed methodology remains unverified pending independent whole-leaf review.

The containing personal-project folder was renamed to `Projects`. Repository identity and existing local work were preserved; registry/trust and agent snapshot dependencies were migrated, and local proofs plus Git whitespace checks pass. No repository implementation changes were required for this rename.

## Inline rewrite and local startup

Implemented kt rewrite ADDRESS CONTENTS with optional --expect, --source and
--dry-run using shared amendment safeguards. Successful writes return the exact
original contents explicitly labeled superseded plus a reminder to restore any
still-valid knowledge lost. New contents are not echoed. No-ops return unchanged
contents with an explicit label; dry-run remains a diff. Mandatory local bootstrap
proof checks and proof-before-reliance rules remain. Editing guidance permits
original-content review through rewrite output, requiring immediate restoration
of lost valid knowledge. No blanket integrity reductions from the interrupted
audit were applied. Root inventories and unrelated-root startup sweeps remain
removed as previously requested.

Amendment/rewrite, CLI, access, bypass/privacy and maintenance tests pass; source
and installed instructions were refreshed locally. Rewrite is canonical throughout
README, bootstrap, lookup/capture/maintenance guidance and hook reminders. Amend
is deprecated in CLI help and retained unchanged for living workers; its old
knowledge route remains a compatibility guide pointing to the rewrite owner.
The owner authorized commit, push and installation. Installer deployment is
complete; installed CLI/handler match source and instruction refresh checks are
clean. The validated changes are committed on main for owner-authorized publication.
Evidence: tools/kt, tests/test-amend.py and focused regression checks, 2026-09-15.
