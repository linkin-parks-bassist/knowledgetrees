---
name: knowledgetrees-ingestion
description: 'Use when ingesting legacy knowledge: find existing owners with kt, establish leaf existence on misses, capture absent answers, audit coverage, and retire redundant sources only when authorized.'
metadata:
  verified_at: '2026-09-12T20:16:19+10:00'
  verified_by: codex /root
  scope: public knowledge-tree example
  source: sanitized operational recommendations and the canonical knowledge-tree contract
  verification: Reviewed kt-first lookup, mandatory miss classification, capture timing, retained root/proof/scope obligations, and installed hardlink identity.
  review_when: Recheck when retrieval gates, bootstrap, or knowledge-tree procedures change.
---

Treat a legacy document as temporary ingestion material, not a parallel canonical
knowledge authority. Establish its coverage boundary and inventory only enough to
bound the work. Process small coherent sections, classifying each substantive
statement as a requirement, decision/rationale, procedure, interface contract,
current-state fact, failure mode, acceptance gate, or other reusable answer.

Write independently retrievable answers into sentence-indexed leaves at the proper
scope. Do not copy the whole document into one leaf, preserve it as the answer, or
leave useful knowledge only as a source path. A provenance line may name the source,
but the leaf body must directly contain the answer. Cross-link shared facts instead
of duplicating them. A summary never establishes coverage of omitted details.

Use `kt find` and `kt open` to find existing owners before adding answers.
If `kt` cannot find an answer, establish whether a leaf exists via alternate terms
and scoped semantic inspection. Amend existing owners; if absent, add the leaf
(or a truthful unresolved record). Preserve an established answer before the next
unrelated tool call. Use `kt proof --root ROOT TOKEN` for affected predicates.
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
