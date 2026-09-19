---
status: green
revised_at: "2026-09-18T13:44:14+10:00"
name: knowledgetrees-ingestion
description: 'Use when ingesting legacy knowledge: find existing owners with kt, establish leaf existence on misses, capture absent answers, audit coverage, and retire redundant sources only when authorized.'
---

Treat a legacy document as temporary ingestion material, not a parallel canonical
knowledge authority. Establish its coverage boundary and inventory only enough to
bound the work. Process small coherent sections, classifying each substantive
statement as a requirement, decision/rationale, procedure, interface contract,
current-state fact, failure mode, acceptance gate, or other reusable answer.

Coverage includes every scale: function-level contracts and rationale,
code-comment-level explanations, file contents, typedef locations, include order,
dependencies and folder structure as well as architecture and specs. Do not let
an architecture summary stand in for omitted implementation details. Checked code
and comments may supply evidence for these answers; their presence in source is
not a reason to exclude useful knowledge from the tree. This coverage requirement
does not itself authorize removing code comments or other source material.

Write independently retrievable answers into sentence-indexed leaves at the proper
scope. Do not copy the whole document into one leaf, preserve it as the answer, or
leave useful knowledge only as a source path. A provenance line may name the source,
but the leaf body must directly contain the answer. Cross-link shared facts instead
of duplicating them. A summary never establishes coverage of omitted details.

Use `kt find` and `kt open` to find existing owners before adding answers.
If `kt` cannot find an answer, establish whether a leaf exists via alternate terms
and scoped semantic inspection. Rewrite existing owners; if absent, add the leaf
(or a truthful unresolved record). Preserve an established answer before the next
unrelated tool call. Use `kt prove --root ROOT TOKEN` for affected predicates.
Compare every substantive section with actual leaf answers. Resolve contradictions
against governing authority and current primary evidence; verify no reusable answer
exists only in the source. Only then, and when authorized, retire the redundant
source and repair references. Keep one knowledge authority rather than synchronized
old/new documentation. Current policy and scope still govern, especially restrictions
on professional or private material entering global or public trees.

If agents assist, divide work into tiny independently reviewable crumbs: one short
section, semantic question, contradiction check, or other bounded item with exact
read/write boundaries. The integrator owns relevance, atomicity, branch coherence,
authority, deprecation, and final coverage decisions, and continues non-overlapping
integration while workers run. Delegation does not transfer those decisions.

For changes to the procedure itself, audit each old obligation against a new direct
answer before shortening bootstrap text. The kt-first rule and miss/capture
obligation must stay self-contained in bootstrap; detail can move to reachable
leaves, but no rule may survive only in
Git history or an unimported source report.
