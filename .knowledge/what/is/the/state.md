---
verified_at: '2026-09-12T12:06:21+00:00'
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
orientation, installs the single verifier, asserts the `AGENTS.md` bootstrap, and
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

Knowledge-tree skill invocation is a once-per-fresh-session bootstrap. A loaded
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
The installer distributes it alongside the single verifier. `tests/test-kt.py` checks isolated
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
the plugin. Codex trust still requires user review through `/hooks`. Live model
behavior remains untested, and this implementation is awaiting publication review.

Installer leaf comparisons ignore only successful proof-marker timestamp refreshes,
preventing a verifier-stamped leaf from conflicting on an idempotent reinstall.
Falsified markers, leaf falsification flags, and all substantive content differences
remain protected; targeted regression checks cover those distinctions.
