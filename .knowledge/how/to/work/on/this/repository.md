---
status: green
revised_at: "2026-09-20T15:05:56+10:00"
---

Use `.knowledge/` for this repository’s operational knowledge and `example/` for the visible distributable corpus. Run `kt prove --local` for the project root and `kt prove --root example` for the specimen. Update each only when its distinct scope requires it. Never put repository requirements, work state, or publication status in `example/`, or use it for project orientation.

Current truth is the first priority. When behavior or evidence changes, identify the owning leaves and reconcile all affected instructions before relying on them or reporting completion. Compare the CLI and tests with README, startup hook payloads, installer templates, public example guidance, local and installed leaves. Read the relevant claims; a passing proof or string search alone cannot establish semantic consistency. Refresh generated and installed copies when authorized and check their drift.

Commit leaf updates in lockstep with the work they describe: every change to `.knowledge/` or `example/` (including a new or rewritten owner leaf) goes in the same commit as the code, tests, and docs it concerns, so no commit leaves knowledge stale and no leaf edit is left uncommitted or deferred to a later documentation commit. Knowledge that lives only in an untracked root (for example the installed global root) cannot be committed, so a leaf that documents repository behavior belongs in `example/`, from which the installer renders the global copy.

Follow the user’s current publication instructions. Earlier authorization for in-scope work persists across turns; do not invent a new per-release approval gate. Repository knowledge is not itself an authorization source.
