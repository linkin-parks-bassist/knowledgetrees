---
status: green
revised_at: "2026-09-21T14:58:05+10:00"
---

Codex discovers the knowledge-tree skills once, from the shared `~/.agents/skills/` catalog. The installer does not create parallel knowledge-tree entries under `~/.codex/skills/`, and it removes the five exact legacy Codex-local copies plus their exact `[[skills.config]]` registrations while preserving unrelated skills and configuration.

The former duplication was caused by installing the same five hardlinked skill entry points into both discovery catalogs. Two stale managed config blocks also explicitly registered `knowledgetrees-capture` and `knowledgetrees-ingestion`. Because Codex scanned both locations, it presented duplicate skills even though paired files had identical content and inode identity.

The installer regression test seeds both classes of duplication and verifies that installation leaves the shared entries present, the Codex-local knowledge-tree entries absent, and all matching explicit registrations removed.
