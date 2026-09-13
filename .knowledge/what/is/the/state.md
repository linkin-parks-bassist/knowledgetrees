---
status: unverified
updated_at: '2026-09-12T12:34:09+00:00'
verified_at: '2026-09-12T12:21:21+00:00'
verified_by: codex /root
scope: knowledgetrees repository
source: direct filesystem, verifier, privacy scan, Git, and GitHub inspection
verification: Ran CLI, installer, shared hook, mock OpenCode adapter, and proof-stamp suites plus all three proof sweeps; reviewed reminder semantics and proof versus leaf validation. Live model adoption remains untested.
review_when: Update after every material repository change.
---

The repository's actual operational knowledge lives in `.knowledge/`. The separate,
visible `example/` corpus contains the canonical knowledge-tree procedure, complete
public-safe generic methodology, and distilled planning and specification leaves.
The knowledge-first installer merges reusable leaves into the user's global root,
preserves local
orientation, installs kt with built-in verification plus its legacy entry point, asserts the `AGENTS.md` bootstrap, and
hard-links shared-harness and Codex skill entry points to the installed canonical
procedure. Skill-shaped entry points are created during installation. Its
isolated-home integration suite passes, as do both repository proof
sweeps. The example orientation remains intentionally empty and the README tells
adopters how to describe their local environment safely. The local repository uses `main`
and tracks the public GitHub remote. The repository owner reviewed the README edits,
and commit `7949a71` was pushed as the first public `main` branch publication. The
example also contains a deliberately terse, metadata-complete Dedekind-complete
ordered-field leaf. `what/leaves/are/distilled/from/superpowers.md` records which
four example leaves carry Superpowers provenance and checks their source count.

Knowledge-tree procedure loading is a once-per-fresh-session bootstrap. A loaded
session continues applying the procedure across messages, turns, and tasks without
reinvocation. Entering another project scope triggers orientation and verification,
not another skill bootstrap.

The README explicitly explains roots in arbitrary directories and nested subsystem
scope as a context-relevance mechanism. It emphasizes verification before reliance,
repair of failing proofs, and executable provability limited to marked predicates.

The verifier stamps each proof outcome separately, marks leaves falsified after a
failed proof or malformed proof structure, and retains that flag until independent
review clears it. Passing proofs never modify leaf verification metadata. Legacy
markers, read-only mode, mixed outcomes, and hardlink preservation have dedicated
integration coverage in `tests/test-proof-stamps.py`.

The README opens with the requested tongue-in-cheek categorical-limit and skeptical
intuitionistic sub-verification tagline.

The bootstrap now carries the kt-first default and miss-resolution obligation inline, with detailed
retrieval, capture, maintenance, and ingestion in direct-answer leaves. The installer
also exposes each procedure as its own hardlinked skill in shared and Codex roots,
enables all five skills, and preserves unrelated permissions. Global and
repository orientations provide concrete entry routes. The installer obtains
informed `[n/Y]` consent before configuring scoped OpenCode reads and knowledge-tree
writes or making any installation changes. Integration checks and read-only proof
sweeps of repository, example, and installed global trees pass.

`tools/kt` is the dependency-free Python lookup and capture CLI, deployed locally under the
global root's `.tools/` and exposed through `~/.local/bin/kt`. It ranks keyword
and quoted-question matches, labels project/global roots, reads leaf metadata,
prints leaves verbatim, and forwards proof roots/options correctly. Question-prefix
navigation consumes directory words, returns exact
leaf hits verbatim, then rank unmatched words only inside the selected branch.
If best non-grammatical keyword coverage is below the default 60% threshold, widen
one parent and retry. Empty or weak-only matches exit 1 while retaining suggestions;
adequate heuristic matches precede weak suggestions. `--min-coverage` tunes the cutoff.
Terminal `_` lists the selected branch. Prefix scoping, exclusion of sibling
branches, exact reads, and incremental widening have isolated CLI test coverage.
The installer distributes its legacy verifier compatibility entry point alongside kt. `tests/test-kt.py` checks isolated
roots with spaces, phrase ranking, metadata, missing results, open scoping, and
proof forwarding without executing real predicates.

`kt add QUESTION ANSWER` (alias `capture`) creates a sentence-derived leaf in one
call, defaults to nearest-project then global scope, and accepts explicit root,
provenance, multiline stdin, dry-run, and unresolved-record options. It refuses
existing owners and unsafe path forms. Creation timestamps and unverified status
are separate from independent whole-leaf review and proof outcomes. Capture never
executes the body or fabricates proofs. Isolated tests cover creation, exact
retrieval of captured answers, repeated question words, overwrite protection,
scope, stdin, previews, unresolved metadata, and path rejection.

All five procedures integrate `kt`. A search/content miss must be resolved as an
existing leaf to retrieve/amend or an absent leaf to investigate/add. Established
answers must be captured before the next unrelated tool call or completion;
verification/capture calls remain allowed. Repository and installed user-wide
bootstrap instructions use the compact rule, while skills retain root, proof,
scope, path, privacy, and maintenance details. Checked loaded answers need no
redundant lookup. Structural checks do not establish behavioral compliance.

Failure and one-shot capture-review hooks are implemented with a shared Python
handler in `tools/kt-hooks` and a thin OpenCode adapter in `tools/kt-opencode.mjs`.
The installer merges Codex definitions without replacing unrelated hooks and
installs dedicated Copilot CLI definitions plus an automatically discovered
OpenCode plugin. Targeted `--hooks-only` updates preserve installed leaf contents,
inodes, skills, and permissions. Session counters and hashed receipts use private
XDG state outside tree payloads; no raw tool logs or knowledge bodies are stored.
Failures remind agents to query kt and capture the eventual reusable diagnosis.
At stop/idle, a failure or 10 completed calls requests one capture-review follow-up;
ordinary user prompts rearm the cycle, synthetic review prompts do not. This is
reminder delivery, not semantic capture verification. Python protocol tests and a
mock OpenCode harness test cover failure context, successful-work thresholds,
deduplication, session isolation, synthetic-loop prevention, and model/agent retention.
Adapters are installed locally; fresh OpenCode configuration discovery includes
the plugin. A live Codex test exposed stdout-only Bash hook transport, which lost
silent failures. The former exit-status bridge has been retired in favor of unwrapped diagnostic heuristics; silent failures remain a documented limitation. The owner supplied a live OpenCode transcript confirming
idle capture review after intentional false, without an invented capture. Scoped
read-only OpenCode database inspection also confirmed metadata exit 1 and the full
failure reminder appended to that stored tool output, although the terminal
transcript hid it. Guidance generation/attachment is confirmed; model compliance
and a separately inspected provider-wire payload are not. Copilot live behavior
remains unconfirmed.
The owner approved publication of this implementation and its diagnostic update.

OpenCode now loads the canonical bootstrap procedure body into one block of each
assembled model system context. It adds no conversation prompts or model turns;
the procedure explicitly avoids repeated skill invocation and startup checks.
Compaction context preserves initialization state and pending captures. Mock SDK
tests cover injection before work, duplicate prevention, rebuilt requests and
separate sessions, and compaction context. The plugin is installed locally; restart
OpenCode for an uncoached live bootstrap test. Other harnesses retain compatibility
skill loading until their startup-context adapters are implemented.

Installer leaf comparisons ignore only successful proof-marker timestamp refreshes,
preventing a verifier-stamped leaf from conflicting on an idempotent reinstall.
Falsified markers, leaf falsification flags, and all substantive content differences
remain protected; targeted regression checks cover those distinctions.

## Unwrapped failure detection

Use unwrapped PostToolUse with structured-status precedence and diagnostic-line
heuristics, plus existing Stop bookkeeping. No pre-tool command rewriting remains;
legacy `codex before` calls are inert. The installer removes only its managed
pre-tool definition and preserves unrelated hooks, including mixed hook groups.

Explicit exit status wins, including zero even when expected error text appears.
Otherwise inspect diagnostic shapes: error/fatal prefixes, compiler error locations,
Python traceback and exception lines, shell command/syntax/path failures, npm,
make/CMake/ninja failures, build-failure markers, and common network/file diagnostics.
Strip ANSI formatting and bound heuristic input to 256 KiB. Plain mentions of
errors, ordinary warnings, and zero-error summaries do not trigger reminders.
This is best-effort detection: silent nonzero Bash exits remain undetectable from
stdout-only transport, and printed or quoted diagnostic examples can false-trigger.

Completed calls and detected failures still update session counters and hashed
receipts. Repeated callbacks are deduplicated; detected failures arm the one-shot
Stop review. Ordinary prompts rearm the cycle; review prompts do not loop.
No raw commands, outputs, or diagnostic bodies are stored. Test coverage includes
positive/negative diagnostics, success precedence, failure deduplication, stop
arming, silent-output limits, and preservation/removal during installer migration.
Source: tools/kt-hooks, install, tests/test-hooks.py, tests/test-install.py;
current Codex live stdout-only payload shape and owner-authorized heuristic tradeoff.

Local deployment verified: an unwrapped SYNTH_BUILD_FAIL diagnostic delivered
the failure reminder and retained exit 1. Hook and installer integration tests passed.

Final validation passed: hook, installer, lookup/capture, proof-stamp, and OpenCode
adapter integration suites; project and example proof sweeps; git diff --check.
The owner authorized publication of this update. No uncertainty hook was added.

## Shared startup orientation

Codex SessionStart and OpenCode system-context bootstrap share the Python startup
loader. It resolves the supplied cwd and reads only that directory’s
.knowledge; it never searches parent directories. It appends where/am/i.md verbatim after the canonical procedure,
labeling the source and retaining the obligation to verify evidence/proofs.
It never substitutes a parent or global orientation when the local file is missing;
missing or oversized (over 64 KiB) orientation reports a diagnostic and retains
the canonical bootstrap. No root means no injected project orientation.
Codex startup/resume/clear/compact events use the same loader; OpenCode loads it
at plugin startup and retains a single block in rebuilt system context.
OpenCode still requires restart after installed plugin/context changes.

Both harnesses share diagnostic failure detection and Stop/idle bookkeeping.
OpenCode tests cover metadata-free diagnostics through tool.execute.after and
terminal tool-part events, explicit exit-zero precedence, and existing one-shot
review/session isolation. No command wrapping or uncertainty scanner is added.
Source: tools/kt-hooks; tools/kt-opencode.mjs; tests/test-hooks.py;
tests/test-opencode-hooks.mjs. Relevant integration checks passed.

Installed handler and OpenCode adapter match repository bytes. Hook, OpenCode
adapter, and installer integration checks passed, along with project/example proof
sweeps and git diff --check. Live OpenCode startup requires a restart to verify.

Privacy boundary: automatic orientation injection is restricted to the supplied
session directory. Parent/home orientations are never searched or used as fallback.
The canonical global procedure remains loaded; this does not inject global orientation.

Local-directory privacy regression tests, Python/OpenCode hook tests, installer
tests, and project/example proof checks passed. Both installed adapters are updated.

## Root access policies

Root discovery uses the explicit current-directory tree, the known global tree,
and a private user-global registry at `~/.knowledge/.tools/roots.json` (KT_CONFIG
overrides the registry path). It never walks parent directories. Configured roots
are not indexed in advance; queries read only permitted roots. Registration saves
only a root name, canonical path and policy. An unfamiliar capture target is
registered with access=ask; registration does not grant wider access or write the
requested leaf until approved. Register deliberately with `kt register NAME PATH`.

Policies are allow, ask and deny. Only the tree in the explicit cwd (or cwd itself when named .knowledge) is local
scope and implicitly permitted unless denied; wider/global/cross-repo roots
need approval by default. An allow root policy opens it to all projects; deny wins.
Private roots can have pairwise project-to-root approvals saved persistently.
Project approvals apply to the exact directory by default. `--subdirectories`
explicitly opts in to descendants; granting from a home directory without that
option cannot authorize all repositories below it.

Use `kt access ROOT` to inspect policy. In the user's own terminal,
`kt access ROOT allow --scope project` saves pairwise trust; --scope all saves
open access; --scope session saves a session decision in private SQLite state.
Session scope needs the same KT_SESSION_ID (or CODEX_THREAD_ID/OPENCODE_SESSION_ID)
in the user's terminal and agent environment. Grants expire after seven days;
distinct session identifiers isolate them. `deny`, `ask`, or `reset` replace or
revoke decisions at the chosen scope. Mutation requires an interactive confirmation;
noninteractive agent lookups never save approvals automatically. Agents must not
supply that confirmation themselves. Retrieval can send content to the configured
model provider. Policies govern kt and startup injection, not direct filesystem reads.

Search, exact questions, relative and absolute open, capture and proof respect
access. Restricted roots expose no leaf paths/snippets/rankings; roots reports
restricted paths as hidden. Registered restricted subtrees cannot leak through
an allowed ancestor; proof rejects scopes containing restricted registered trees.
Blocked access exits 3, is not an answer lookup miss, and does not imply absence.
Malformed configuration fails closed. Registry writes are atomic and private;
installer updates preserve the user registry. Both harnesses share policy loading
and startup suppression for denied local orientations.

Evidence: tests/test-access.py checks no content leakage, persistent/new-process
approvals, cross-project isolation, exact/opt-in descendant behavior, session
isolation, revoke/deny/open override, private capture registration, absolute paths,
and nested restricted roots. Existing CLI, hook, OpenCode adapter and installer
suites pass with explicit access fixtures. Fixture adjustments reflect the new
privacy defaults; old globally-open discovery is intentionally superseded.

Installed CLI, shared handler, and procedural leaves match the repository. Access,
CLI, hook, installer, proof-stamp and OpenCode adapter tests passed; project, example
and global proof sweeps passed before deployment. No root access grants were saved
on the user’s behalf. Both harnesses use the same registry and privacy policies.

Additional regression: starting in a private registered tree’s subdirectory does
not grant its entire ancestor scope. Exact-directory scope stays the default;
descendant project inheritance requires the explicit --subdirectories option.

## Revision-checked amendment

Read a leaf with `kt open ROOT:PATH --revision`. stdout remains the complete
verbatim Markdown; stderr supplies `Revision: <SHA-256>` for those same bytes.
Write a complete revised version to a temporary file and submit it with
`kt amend ROOT:PATH --expect HASH --body-file FILE`. Omit --body-file or use `-`
to read the replacement from stdin. `--dry-run` shows the resulting diff without
writing. Optional --source records actual new evidence.

The command needs no Git repository and invokes no editor. Revision mismatch exits
4 and leaves the file untouched; reread and merge concurrent changes. An advisory
exclusive lock serializes amend writers, and a final content/inode check detects
ordinary intervening edits by non-locking writers. This is not transactional against
arbitrary direct file writes or power loss. In-place writes preserve hardlinks.
Access policies apply to reading and amendment; symlink aliases cannot be amended.

Identical submissions are no-ops unless new source is supplied. Changed content
loses whole-leaf verified_at, verified_by and verification fields and becomes
unverified (or remains unresolved). updated_at records editing, not verification.
Unchanged assertion-paragraph plus fenced predicate retains its original proof
marker, regardless of any replacement timestamp supplied. New or changed proofs
are reset to `Proof: (verified at _)` and must be checked separately. Amendment
never executes proof bodies or claims independent whole-leaf verification.
Sticky falsified_at is preserved even if omitted from the replacement; independent
review/repair remains necessary before deliberately clearing it.

Evidence: tests/test-amend.py uses a standalone non-Git tree and verifies conflict
refusal, dry-run/no-op behavior, in-place hardlinks, review invalidation, unchanged
and changed proof stamps, sticky falsification, stdin/body-only text, input validation,
symlink refusal, and denied-root behavior. Existing lookup and access tests pass.

Amendment, lookup, access, installer, Python hook and OpenCode adapter suites pass.
The installed CLI and hardlinked capture procedure are updated. Newly inserted
orphan proof markers cannot retain caller-invented verification timestamps.

## Proof command rename

The CLI command is now kt prove throughout implementation, help, tests and
distributed/installed procedural leaves. The old proof subcommand is rejected.
All seven integration suites passed; CLI copies are installed. Proof remains
the noun for evidence and proof markers, not a renamed artifact type.

## Access confirmation

The access prompt uses `[y/N]`, accepts `y` or `yes` case-insensitively, and
defaults to no. The access integration suite checks the prompt, short affirmative
answers, empty/negative/invalid responses, and unchanged registry on refusal.
The installed CLI is updated without changing access grants.

OpenCode resume guidance is documented in the README and canonical hooks leaf.
Official startup/CLI documentation and adapter code support activation after a
full process restart, including older sessions; historical calls are not replayed.
A separate backend must also restart. Live resume adoption remains unverified.
The owner authorized committing and pushing the confirmation and documentation update.

Access, CLI, and OpenCode adapter integration checks, project/example read-only
proof sweeps, and diff whitespace validation pass for this update. Installed
access and hooks documentation is updated without overwriting customizations.

## Built-in proof verification

`kt prove` now runs its built-in proof engine after the existing root access
checks; it needs no standalone verifier executable. The legacy standalone name
is a compatibility entry point into that same engine and preserves its old root
selection semantics without kt access enforcement. New integrations use kt prove.
CLI tests execute real proofs without a separate installed verifier, and the
proof-stamp suite passes through both entry points, covering hardlinks, mixed
outcomes, read-only checks, legacy markers, and sticky falsification.

The owner requested compact agent-oriented default output with opt-in `--pretty`.
Existing canonical CLI usage lives in example/how/to/use/kt.md; update that owner
and the installed usage leaf rather than creating a parallel answer.

Non-exact lookup defaults to compact plain-text rows with lexical coverage,
weak/falsified status, root-qualified addresses, and excerpts bounded to 160
characters. `--pretty` restores the human layout and opt-in terminal colors.
Exact answers remain verbatim. Default roots, capture, and orientation previews
are also compact. Usage documentation replaces stale parent-discovery and
verifier-forwarding descriptions with current behavior.

Final checks pass: access, lookup/capture, amendment, installer, shared hooks,
OpenCode adapter, and proof stamps through both the compatibility and built-in
entry points. Project, example, and installed global proof sweeps pass. The
installed CLI and compatibility entry point match repository bytes; relevant
installed procedure edits preserve hardlinks. Publication is owner-authorized.
