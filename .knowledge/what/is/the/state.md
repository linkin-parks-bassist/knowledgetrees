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

## Revision-carrying reads and inline rewrite

Full open/exact-question reads automatically return a SHA-256 revision on stderr
for the same bytes read on stdout. kt rewrite ADDRESS HASH CONTENTS requires that
revision positionally; no rewrite --expect. Conflicts preserve the leaf. Success
is silent on success and identical no-ops (exit 0), echoing neither body. The existing one-shot
capture-review hook carries the accuracy/preservation reminder once per work cycle. No-op
output is brief; dry-run remains a diff. Original contents must be in context
before editing. Mandatory proof checks remain intact. Deprecated amend retains
its required --expect syntax and behavior for living workers. Root inventory and
unrelated-root startup sweeps remain removed. Guidance and README reflect this
contract. The preceding version was published as f230b4d; this interface update
is not yet published. Local installation and instruction refresh are complete;
CLI, amendment/rewrite, access, bypass/privacy, maintenance, installer and harness
hook tests pass. Project, installed global and public example proof checks pass.
Evidence: source and regression/proof checks, 2026-09-15.

Legacy amend CLI calls now emit a brief deprecation notice on stderr pointing
to the updated rewrite procedure. Rewrite/internal combine calls stay free of
that notice; legacy stdout and behavior are preserved.

The deprecation notice is installed locally with refreshed guidance. Amendment
and maintenance tests plus project/global proof checks pass; publication remains
pending alongside the positional-hash rewrite changes.

Silent rewrite and one-shot preservation-reminder changes are installed locally.
Focused amendment and hook tests plus project/global proof checks pass; the
follow-up interface work remains uncommitted.

Normal operation follows kt prove: mutation success/no-ops are silent, with
requested data/previews, errors and consent prompts retained. Legacy amend
continues its compatibility stdout plus deprecation notice.

The normal-success silence policy is installed locally and reflected in README,
usage and bootstrap. CLI, amendment, maintenance, access, bypass/privacy and
installer regressions pass; project/global/example proofs pass. Executables match
source and instruction refresh checks are clean. Follow-up changes are uncommitted.


kt dict now prints sorted unique useful accessible leaf-path segments on one
comma-separated line without reading bodies or exposing full paths. It filters
two-character and standard grammar/navigation segments. Optional configured roots restrict its scope. The
bootstrap, installer block, README and usage require one fresh-session dictionary
call. CLI tests cover deduplication, ordering, hyphen preservation, root selection
and restricted subtree exclusion. This work is not yet installed or published.

The dictionary implementation is installed locally. Installed and source output match for the current accessible roots.
Curated guidance is synchronized; installed executable matches source. CLI,
access, bypass/privacy, rewrite/amend, maintenance, installer, hook and proof-stamp
tests pass. Project, installed-global and public-example proofs pass. Dictionary
publication remains pending with the other uncommitted follow-up changes.

Capture review found and removed a duplicated “check.” fragment in the one-shot
review prompt. Hook regression coverage now rejects its return. The corrected
handler is installed locally; publication remains pending.


The owner authorized aligning local installed guidance with the latest canonical
repository example. A full forced install replaced all 51 reusable leaves, deployed
CLI/hooks/skills/bootstrap and preserved the existing orientation. Installed-global
proofs pass and installed kt matches source. The dictionary now emits 514 filtered
segments in one comma-separated line for current accessible roots. Manual refresh
scope rendering matches the installer and its drift check ignores successful proof
timestamp refreshes. Publication remains pending.


The full install exposed a Codex TOML merge defect: ENABLED_SETTING used `\s*$`,
consumed following newlines and joined three skill entries to subsequent tables.
The live config was repaired and parses with 13 skill entries. The regex now accepts
horizontal trailing whitespace only, the installer parses proposed TOML before
writes, and an adjacent-table regression test passes. All ten installed KT skill
paths have required frontmatter and point to their canonical hardlinks. A client
reload is still needed to clear the warning shown before repair.


The owner authorized committing and publishing the complete follow-up. Final
validation passed for CLI, rewrite/amend, maintenance, access, bypass/privacy,
installer, Codex/OpenCode hooks and proof timestamps. Project, installed-global and
public-example proofs pass. The installed 51-leaf canonical corpus matches current
rendered repository guidance; Codex TOML parses with 13 skill entries; installed kt
matches source. The validated work was committed and pushed to main as 4c8e553. The local
installation already matches the published implementation and guidance.


Bare kt prove now checks all accessible roots; --local and --global provide readable
single-root selectors. Bootstrap uses --local. CLI tests distinguish local/global
selection and prove that bare mode observes a failure in another accessible root.
This follow-up is not yet validated, installed, committed or published.


The proof-selection follow-up is validated and installed. Bare kt prove checks all
accessible roots; --local and --global narrow explicitly, and bootstrap uses
--local. Full regressions and actual local/global/all-accessible proof sweeps pass.
Installed kt matches source and guidance drift is clean. The completed proof-scope follow-up was committed and pushed to main as 18eea6f.


kt dict now walks accessible directory trees directly and considers only the
containing-directory name and leaf stem. It rejects short and grammar/navigation
segments before inserting candidates into its deduplicating set; registered nested
roots are pruned at directory boundaries and traversed separately when accessible.
This preserves pairs such as obtain/sudo-authorization while dropping most shared
structural vocabulary. The optimized output is byte-for-byte identical to the
prior final-two implementation: 215 segments and 2,237 bytes for the current roots.
Seven warm source runs measured a 0.197-second median, down from about 0.62 seconds
before the specialized traversal. CLI, access, bypass/privacy, installer, leaf
maintenance, hook and proof-stamp regressions pass. Project, global and public
example proofs pass; installed kt matches source and guidance drift is clean. The
completed dictionary optimization and guidance were committed and pushed to main
as 6bb5098.

Green/yellow/brown lifecycle support is implemented in the repository source.
`expires_at` accepts timezone-aware ISO 8601; `expires_every` accepts compact or
plain-English seconds-through-weeks durations measured from `verified_at`. `kt prove`
aggregates all selected roots, always prints the three totals, prints every yellow
or brown root-qualified leaf, warns without failing for yellow, and fails for brown.
All regression suites pass. Public guidance and the project spec are updated. Local,
public-example, and installed-global proof sweeps have no brown leaves. Installation
is complete and the installed executable matches repository source. The first install
surfaced a sticky global falsification caused by a nondeterministic Copilot discovery
predicate; the predicate was removed from its two global owners after deterministic
topology checks and repeated full proof sweeps passed. The owner subsequently
authorized installation, commit, and publication.

The lifecycle default is corrected: leaves without explicit lifecycle metadata are
green, including non-verifiable specs, plans, procedures, and opinions. Yellow now
requires `state: yellow` or elapsed expiry metadata; unverified workflow status does
not imply yellow. Expiry guidance targets factual knowledge liable to change. All
regression suites pass; installation is current and byte-identical to repository
source. Final proof sweeps report project `green=25 yellow=0 brown=0`, example
`green=56 yellow=0 brown=0`, and global `green=104 yellow=0 brown=0`.

The lifecycle feature and green-default correction are installed and published on
`main` as commits `c0e9e54` and `efb5809`. No lifecycle implementation,
installation, or publication work remains.
