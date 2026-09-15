---
scope: knowledgetrees repository
source: "tools/kt built-in proof engine; installer; owner removal of separate verifier"
review_when: Recheck when installer behavior, target paths, or test coverage changes.
status: "unverified"
updated_at: "2026-09-13T13:54:30+10:00"
---

Run `python3 -B tests/test-install.py`. The test uses temporary target homes and
checks dry-run behavior, knowledge installation, spine exclusion, empty-orientation
creation and preservation, existing `AGENTS.md` and Codex configuration preservation,
idempotency, conflict refusal, forced replacement, verifier execution, and same-device
same-inode hard links for both compatibility skill entry points. It also rejects a
regression to per-task skill invocation in the installed procedure or `AGENTS.md`.

Hook integration also checks safe Codex merge, malformed-hook refusal before writes,
dedicated Copilot event definitions, OpenCode adapter deployment, idempotent hook
installation, and `--hooks-only` preservation of customized leaves, hardlinks, and
permissions. Run `python3 -B tests/test-hooks.py` for shared protocol tests and
`node tests/test-opencode-hooks.mjs` for the mocked OpenCode adapter. Neither runs
models. Run `python3 -B tests/test-kt.py` for retrieval and weak-result exit checks.

Successful proof timestamp refreshes alone are not installation content conflicts;
their installed stamps are retained until the verifier checks them again. Falsified
markers, sticky leaf falsification flags, prose edits, and other metadata changes
remain protected content differences. Reinstallation tests cover both cases.


Codex skill enablement must preserve the newline between an `enabled` setting and
the following TOML table. Match horizontal trailing whitespace only; `\s*$` can
consume the newline and produce invalid text such as `enabled = true[desktop]` or
`enabled = true[[skills.config]]`. Parse the complete proposed configuration with
Python tomllib before any installer write. The integration fixture places a desktop
table immediately after an existing disabled skill and verifies the parsed table.
Evidence: repaired ~/.codex/config.toml, install and tests/test-install.py, 2026-09-15.
