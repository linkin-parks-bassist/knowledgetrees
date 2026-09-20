---
status: green
revised_at: "2026-09-20T15:15:55+10:00"
---

This is the project knowledge root for the `knowledgetrees` public repository maintained in this working directory.

The repository explains knowledge trees and provides a visible `example/` tree
containing knowledge-tree material plus adapted planning, specification, update,
and clarification guidance. The `install` script installs that knowledge first and
creates skill-shaped hard links in supported harnesses for bootstrap compatibility.
The repository has been reviewed by its owner and published to the public GitHub
remote.

Use `what/is/the/spec.md` for the acceptance contract, `what/is/the/plan.md` for the
approved workflow, `what/is/the/state.md` for checked present state, and
`what/is/next.md` for the next action. The public `example/where/am/i.md` is deliberately empty for adopters; it is
not an operational orientation.

## How to navigate this tree

- `how/` contains repository procedures: `how/to/work/on/this/repository.md`,
  `how/to/test/the/installer.md`, and `how/to/test/proof/stamps.md`, and
  `how/to/update/installed/kt/instructions.md`; architecture lives in `how/is/kt/structured.md`.
- `what/` owns requirements and progress: `what/is/the/spec.md`,
  `what/is/the/plan.md`, `what/is/the/state.md`, and `what/is/next.md`.
- `where/` establishes repository scope through `where/am/i.md`.
- `why/` explains layout through `why/is/the/example/visible.md`, and lookup latency through
  `why/is/kt/slow/on/a/miss.md`.

Harness integration (startup and failure hooks for four CLIs, and the MCP tools) is documented in the distributable `how/to/use/knowledgetree/hooks.md` and `how/to/expose/structured/knowledge-tree/edits/across/local/agent/harnesses.md`; its repository-specific state is in `what/is/the/state.md`.

Reusable procedures live in the global root and distributable `example/`, not in
this repository's project-state leaves.

- `does/` answers yes/no repository behavior questions through
  `does/this/repository/require/publication/approval.md`.
- `is/` answers yes/no classification questions through
  `is/the/example/the/operational/knowledge/root.md`.
