---
status: green
revised_at: "2026-09-27T14:44:12+10:00"
---

Use `.knowledge/` for this repository’s operational knowledge and `example/` for the visible distributable corpus. Run `kt prove --local` for the project root and `kt prove --root example` for the specimen. Update each only when its distinct scope requires it. Never put repository requirements, planned work, or publication status in `example/`, or use it for project orientation. Keep the CLI, README, public `example/` guidance, installed global guidance, and operational `.knowledge/` aligned with the flat leaf metadata contract.

Current truth is the first priority. When behavior or evidence changes, identify the owning leaves and reconcile all affected instructions before relying on them or reporting completion. A brown leaf is a priority-one incident even at idle startup: the first response reports it to the user, then all work is limited to diagnosis, remediation, and re-checking until brown clears or the user explicitly permits ignoring that specific status. Compare the CLI and tests with README, startup hook payloads, installer templates, public example guidance, local and installed leaves. Read the relevant claims; a passing proof or string search alone cannot establish semantic consistency. Refresh generated and installed copies when authorized and check their drift.

For each change:

1. Repair any known stale or contradictory active knowledge first. Locate its owner, check current evidence, and preserve still-valid content.
2. Change the CLI and focused regression coverage together.
3. Build an affected-owner inventory covering narrow and central procedures, policy/access guidance, spec and plan, README and CLI help, startup payloads, public example, generated surfaces, and installed guidance. Search positively for the new behavior and negatively for superseded counts, lists, fallbacks, and limitations; read every hit in context and repair all owners. Only then run the Python and OpenCode suites plus `git diff --check`.
4. Run `kt prove --no-stamp` across affected roots. Any brown result is a priority-one incident: immediately report it to the user, stop unrelated work, diagnose and remediate the mismatch, and re-check until brown clears; ask the user if safe remediation cannot be established. Continue past brown only with explicit permission to ignore that specific status. Manually review expired yellow leaves before relying on them.
5. Preview installation, install authorized changes, refresh curated instruction copies with `how/to/update/installed/kt/instructions.md`, and check installed bytes and proof results.
6. Update `what/is/the/plan.md`: remove completed steps and add newly planned ones. Then publish under the user’s current authorization, including earlier in-scope instructions.

Commit leaf updates in lockstep with the work they describe: every change to `.knowledge/` or `example/` (including a new or rewritten owner leaf) goes in the same commit as the code, tests, and docs it concerns, so no commit leaves knowledge stale and no leaf edit is left uncommitted or deferred to a later documentation commit. Knowledge that lives only in an untracked root (for example the installed global root) cannot be committed, so a leaf that documents repository behavior belongs in `example/`, from which the installer renders the global copy.

Follow the user’s current publication instructions. Earlier authorization for in-scope work persists across turns; do not invent a new per-release approval gate. Repository knowledge is not itself an authorization source. Preserve access policy and archived trees.
