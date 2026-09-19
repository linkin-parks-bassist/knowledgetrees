---
status: "unverified"
scope: public knowledge-tree example
source: "tools/kt built-in proof engine; installer; owner removal of separate verifier"
review_when: Recheck when installer behavior or harness skill discovery changes.
updated_at: "2026-09-13T13:54:30+10:00"
---
Status: Green

From a complete repository checkout, run `./install`. Preview the targets without
writing with `./install --dry-run`. The installer merges reusable example leaves
into `~/.knowledge` without installing the example's illustrative spine, preserves
an existing `where/am/i.md`, installs the unified CLI at
`~/.knowledge/.tools/kt` (including `kt prove`), and asserts the mandatory
bootstrap in `~/AGENTS.md`.

For a new root, it seeds truthful generic navigation in `where/am/i.md`; add
verified local environment facts. Before any writes, OpenCode configuration changes
require informed `[n/Y]` consent: reads of `~/.knowledge/**` and `~/.agents/**`,
writes to `~/.knowledge/**`, and possible model-provider exposure are disclosed.
Edits to `.agents/**` remain approval-gated. Declining or EOF cancels without changes.
Read `how/to/allow/knowledge-tree/access/in/opencode.md` for permission semantics.

That bootstrap invokes the compatibility skill once at the start of a fresh agent
session. The loaded procedure remains active across messages, turns, and tasks;
reinvocation is reserved for a new session or genuine loss of the procedure from
context.

Current agent harnesses still need a skill-shaped bootstrap. The installer creates
both `~/.agents/skills/knowledgetrees/SKILL.md` and
`~/.codex/skills/knowledgetrees/SKILL.md` as hard links to the canonical installed
leaf at `~/.knowledge/how/to/use/knowledgetrees.md`. It also enables the Codex entry
in `~/.codex/config.toml`. The three paths share one inode, so editing the canonical
leaf cannot leave a wrapper or copied skill body stale.

Four procedure skills are also installed in both roots:
`knowledgetrees-lookup`, `knowledgetrees-capture`, `knowledgetrees-maintenance`,
and `knowledgetrees-ingestion`. Each hardlinks to the respective retrieval,
capture, maintenance, or ingestion leaf, with discovery metadata in that canonical
leaf. All five skills are enabled in Codex configuration and OpenCode permissions.
Quit and restart clients after installation or updates to refresh their catalogs.

Installation is idempotent when installed content is unchanged. Differing existing
leaves or bootstrap skill bodies cause a preflight failure; inspect the differences
before using `--force`. The orientation leaf is preserved even with `--force`.
Hard links require the relevant destinations to be on the same filesystem.
