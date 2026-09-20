---
status: green
revised_at: "2026-09-20T10:05:01+10:00"
---

The repository's operational knowledge root is `.knowledge/`; `example/` is the
public distributable specimen. The example orientation is intentionally empty.
The CLI, README, public guidance, and installed global guidance use flat leaf
metadata. The installed executable matches repository source.

## Implementation

`tools/kt` is the dependency-free Python CLI for lexical lookup, capture,
revision-checked rewrite and maintenance, root access, and proof evaluation.
Full reads return a SHA-256 revision for positional `kt rewrite ADDRESS HASH
BODY`; successful mutations are normally silent. Add and rewrite accept answer
bodies, generate status/revision time, and set expiry or complete proof coverage
through CLI options. Rewrite preserves omitted optional metadata and offers flags
to clear expiry or verifiability. Lookup caches only within
an invocation and never indexes private roots. Force-private wins over grants
and bypass. Registered nested roots remain distinct. `kt boot` prints the
global procedure, exact local orientation, dictionary, and local proof summary;
`kt init` creates an empty local tree and spine.

Leaf front matter has `status` and `revised_at`; optional fields are manual
`checked_at`, `expires_at`, `expires_every`, and `verifiable`. Harness skill
entry points may also have `name` and `description`. All timestamps need an
ISO 8601 timezone. `kt check` records a manual whole-leaf review; `kt prove`
updates status and individual proof markers without advancing that time.
Expired leaves are yellow and appear only in the summary count. Brown is sticky
until manual review or, for a fully proof-covered `verifiable: true` leaf,
all proofs pass. The coverage flag requires author review; passing individual
proofs otherwise do not check a whole leaf. Unsupported front matter is
rejected by writes and reported brown by proof checks. Substantive evidence,
origins, caveats, unresolved blockers, and next checks belong in the answer.

Combine concatenates answer bodies in order, resets manual review time, and
retains brown status from any brown source. Multi-file cleanup is not
transactional; interrupted cleanup needs inspection. The installer merges
curated public guidance while preserving personal orientation and access
registry, and hardlinks skill entry points across supported harnesses. The
local untracked `sync-kt-instructions.py` refreshes curated installed guidance.
Codex/OpenCode share boot and capture-review hooks. Codex native hook trust
and an OpenCode backend restart are needed to load hook changes. A nonblocking
before-tool reminder cannot guarantee review before an already issued command;
actual model compliance is less established than protocol tests.

## Validation and on-disk state

All 11 existing active, non-private registered roots were audited: 1,153
nonempty leaves have flat allowed headers, valid timezone timestamps, and no
bare proof markers. Each root's read-only proof sweep reports zero yellow and
zero brown leaves. A one-time in-place cleanup affected 179 leaves; backup and
post-change hashes, answer bodies, and inodes were audited. Seventeen answers
gained their existing unresolved blocker/next-check text, and one date-only
manual-check record became a factual answer note without inventing a time. The
external backup manifest is at
`/home/david/.local/share/knowledgetrees/metadata-backups/2026-09-20-hard-break/manifest.json`.
A repeat cleanup preview found zero changes. Archived snapshots and force-private
roots were outside the active-root audit. One registered agent-ecosystem root
is absent on disk. The access registry was unchanged.

The preceding metadata cleanup was published as `367d481` and `2b36a74`.
The body-only add/rewrite interface, expiry/verifiability options, tests, README,
and public guidance are now updated. Python and OpenCode suites pass. An install
with `--no-hooks` deployed the CLI and guidance while leaving two pre-existing
user hook edits untouched. Project, public example, and installed-global proofs
are green; installed CLI bytes match source and instruction sync has zero drift.
The validated change was committed and pushed to `origin/main` as `54c461a`.
