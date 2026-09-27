---
status: green
revised_at: "2026-09-27T14:45:19+10:00"
---

This is the project knowledge root for the `knowledgetrees` public repository maintained in this working directory.

The repository explains knowledge trees and provides a visible `example/` tree
containing knowledge-tree material plus adapted planning, specification, update,
and clarification guidance. The `install` script installs that knowledge first and
creates skill-shaped hard links in supported harnesses for bootstrap compatibility.
The repository has been reviewed by its owner and published to the public GitHub
remote.

Use `what/is/the/spec.md` for the acceptance contract and `what/is/the/plan.md` for
the frontier of planned steps, next first. The public `example/where/am/i.md` is deliberately empty for adopters; it is
not an operational orientation.

## How to navigate this tree

- `how/` contains repository procedures: `how/to/work/on/this/repository.md`,
  `how/to/test/the/installer.md`, `how/to/test/proofs.md`, and
  `how/to/update/installed/kt/instructions.md`, and `how/to/audit/public/content/before/publishing.md`; architecture lives in `how/is/kt/structured.md`.
- `what/` owns requirements and planned work: `what/is/the/spec.md` and
  `what/is/the/plan.md`.
- `where/` establishes repository scope through `where/am/i.md`.
- `why/` explains layout through `why/is/the/example/visible.md`, and lookup latency through
  `why/is/kt/slow/on/a/miss.md`.

Harness integration (startup and turn-end maintenance hooks for four CLIs, and the MCP tools) is documented in the distributable `how/to/use/knowledgetree/hooks.md` and `how/to/expose/structured/knowledge-tree/edits/across/local/agent/harnesses.md`; its repository-specific contract is in `what/is/the/spec.md`.

Reusable procedures live in the global root and distributable `example/`, not in
this repository's spine leaves.

- `does/` answers yes/no repository behavior questions through
  `does/this/repository/require/publication/approval.md`.
- `is/` answers yes/no classification questions through
  `is/the/example/the/operational/knowledge/root.md`.
