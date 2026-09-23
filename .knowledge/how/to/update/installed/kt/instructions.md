---
status: green
revised_at: "2026-09-24T08:16:39+10:00"
---

From this repository directory, refresh installed guidance before deploying executables:

1. Complete the affected-owner inventory required by `how/to/use/knowledgetrees.md` and `how/to/maintain/a/knowledge/tree.md`. Prove the edited local and public-example roots first so lifecycle metadata in the source leaves is canonical before comparison or copying.
2. Run `python3 sync-kt-instructions.py --check` to compare the curated, proved source leaves with installed global leaves and skill hardlinks.
3. If guidance changed, run `python3 sync-kt-instructions.py`. Replaced content is backed up under `~/.local/state/knowledgetrees/instruction-backups/`.
4. Run `./install --dry-run --force`, inspect its scope, then run `./install --force` to deploy the CLI, hooks, MCP server, harness registrations, non-core leaves, and skills. The installer proves the installed global root.
5. Prove any affected source root changed since step 1, then re-run the sync check and compare installed `kt` and `kt-mcp` byte-for-byte with this checkout. Zero drift is required before completion.
6. Restart clients or start fresh sessions so they reload tools, hooks, and instructions.

The Git-excluded sync script owns its current `LEAVES` and `SKILLS` sets; do not copy their counts into this leaf. It renders public-example scope as personal-global scope and normalizes successful proof timestamps during comparison, but it deliberately compares lifecycle status. Proving an installed copy can canonicalize its status serialization, so prove the edited source first; if drift still looks status-only, inspect both leaves and establish which copy is current rather than blindly overwriting either one.

Repository and installed leaves have separate inodes; installed rewrites cannot alter public source. Personal leaves, orientations, project spines, unrelated configuration, and unrelated access policy are preserved. The sync does not deploy executables or every installer-managed leaf, and the installer does not replace the sync's backup step, so both operations are required when guidance and tools change. The installer removes only its formerly managed home `AGENTS.md` block and preserves unrelated instructions.

Zero byte drift proves copying consistency, not semantic freshness.
