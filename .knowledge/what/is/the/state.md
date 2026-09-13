---
status: "unverified"
scope: knowledgetrees repository
source: "Read-only local source-byte, launcher, hook-output, skill-inode and registry checks; final captured-knowledge audit"
review_when: Update after material repository changes.
updated_at: "2026-09-13T13:52:27+10:00"
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
from handler dispatch; the built-in proof engine is a contiguous section. The
legacy verifier is only a compatibility entry point into that engine and also
respects force-private.

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
maintenance/coalescing, installer, shared hooks, OpenCode adapter, and both proof
entry points. All suites passed after the refactor. Read-only proof sweeps passed
for the project, installed global root, and public example. The CLI, compatibility
verifier, and shared hook handler are deployed with identical source bytes; the
access registry was unchanged. The owner-authorized implementation update was committed and pushed to main
as 8e7a24b. A native rewrite remains a possible future optimization, contingent
on larger-corpus and warm/cold timing measurements.

Final local installation audit: PATH launcher resolves to the installed kt; kt,
the compatibility verifier and handler match repository bytes and are executable.
OpenCode plugin bytes and every managed Codex/Copilot hook definition match the
installer output. The five procedure leaves retain both harness skill hardlinks;
canonical branches and the home AGENTS bootstrap are present. Persistent bypass
is disabled. This verifies on-disk installation, not whether an existing OpenCode
backend has reloaded its plugin or a model will comply. The final knowledge audit
corrected old verifier guidance, startup privacy wording, and installed skill scope
labels; changed leaves remain unverified pending independent whole-leaf review.
