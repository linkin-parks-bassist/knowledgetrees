---
verified_at: '2026-09-12T13:51:10+10:00'
verified_by: codex /root
scope: public knowledge-tree example
source: distilled from Superpowers 6.3.0 brainstorming and spec-review methodology
verification: Compared the leaf with the quarantined specification review loop and the knowledge-tree current-truth rule.
review_when: Recheck when specification maintenance practice changes.
---

Reread the current specification before editing it. Determine whether new evidence
changes a governing requirement, resolves an ambiguity, narrows scope, or merely
records implementation history. Update the current owner in place; do not append a
chronological correction that leaves incompatible instructions active.

After the edit, check for placeholders, contradictions, ambiguity that could produce
different implementations, accidental scope growth, and requirements that no longer
fit the architecture or acceptance criteria. Update affected plan tasks and current
state projections when the specification change alters implementation work. Keep
historical rationale only when it still explains a live decision or constraint; rely
on version control for superseded wording.
