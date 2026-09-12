---
verified_at: '2026-09-12T13:51:10+10:00'
verified_by: codex /root
scope: public knowledge-tree example
source: distilled from Superpowers 6.3.0 writing-plans methodology
verification: Compared the leaf with the quarantined writing-plans skill and retained its reusable planning guidance without its harness-specific workflow.
review_when: Recheck when implementation-planning practice changes.
---

Start from an approved specification or a clearly bounded requirement. If the work
contains independent subsystems, split it into separately useful plans before adding
detail. State the goal, architectural approach, technology constraints, governing
specification, and global constraints at the top.

Map the files to create or change and give each one a clear responsibility. Divide
work into independently testable tasks whose boundaries a reviewer could
meaningfully approve or reject. Within each task, name exact files and interfaces,
then write concrete steps: create the failing test, run it and observe the expected
failure, implement the smallest sufficient change, rerun the relevant checks, and
commit the coherent result. Fold scaffolding, configuration, and documentation into
the task whose deliverable requires them.

Do not leave `TBD`, `TODO`, “add validation,” “write tests,” or references to
undefined interfaces. Finish by checking every specification requirement against a
task, scanning for placeholders, and confirming that names and types agree across
task boundaries. A plan should let an unfamiliar competent implementer proceed
without guessing, while avoiding unrequested design.
