---
status: green
revised_at: "2026-09-27T14:41:16+10:00"
---

A **knowledge root** is a `.knowledge/` directory that anchors one semantically
navigable knowledge tree for a defined scope. Examples include the personal global
root `~/.knowledge`, a repository's `.knowledge`, and a narrower subsystem's
`.knowledge`.

Knowledge roots compose federatively: use the nearest applicable root first, then
broader roots as needed. Every knowledge root must contain a maintained
`where/am/i.md` as its guaranteed orientation and README-equivalent entry point,
plus the canonical `how/`, `what/`, `where/`, `why/`, `does/`, and `is/` branches. Neutral roots
do not assume a project lifecycle. Repository project roots additionally contain
`what/is/the/spec.md` and `what/is/the/plan.md`; `kt init --project` creates those
placeholders explicitly.

Every semantic payload file is a Markdown leaf whose path is derived from the full
natural-language question it answers by replacing spaces with `/`. Directories are
semantic routing only; scripts and other non-leaf artifacts do not belong below a
knowledge root. Run the proof verifier without tokens for a whole-root check and
with exact semantic path-component tokens for focused checks.
