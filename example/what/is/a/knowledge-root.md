---
verified_at: '2026-09-12T13:51:10+10:00'
verified_by: codex /root
scope: public knowledge-tree example
source: sanitized adaptation of the canonical global knowledge-tree methodology
verification: Compared the generic answer with the installed knowledgetrees procedure and removed host-specific provenance.
review_when: Recheck when the knowledge-tree model or operating procedure changes.
---
Status: Green

A **knowledge root** is a `.knowledge/` directory that anchors one semantically
navigable knowledge tree for a defined scope. Examples include the personal global
root `~/.knowledge`, a repository's `.knowledge`, and a narrower subsystem's
`.knowledge`.

Knowledge roots compose federatively: use the nearest applicable root first, then
broader roots as needed. Every knowledge root must contain a maintained
`where/am/i.md` as its guaranteed orientation and README-equivalent entry point,
plus the canonical `how/`, `what/`, `where/`, and `why/` branches. Repository roots
also contain `what/is/the/spec.md`, `what/is/the/plan.md`,
`what/is/the/state.md`, and `what/is/next.md`.

Every semantic payload file is a Markdown leaf whose path is derived from the full
natural-language question it answers by replacing spaces with `/`. Directories are
semantic routing only; scripts and other non-leaf artifacts do not belong below a
knowledge root. Run the proof verifier without tokens for a whole-root check and
with exact semantic path-component tokens for focused checks.
