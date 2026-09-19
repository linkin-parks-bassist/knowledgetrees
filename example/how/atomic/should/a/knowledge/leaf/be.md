---
scope: public knowledge-tree example
source: "Owner explicit all-scales knowledge requirement; canonical procedure review, 2026-09-14"
review_when: Recheck when the knowledge-tree model or operating procedure changes.
status: unverified
---
Status: Green

Semantic atomicity is guidance, not a maintenance rule. A reasoning agent decides in
context whether two related pieces of knowledge belong in one leaf or two. Relevant
considerations include how strongly they are related, how an uncertain agent is
likely to discover them, whether they are normally needed together, and whether they
share an owner, volatility, review condition, proof predicate, or reuse pattern.
Branch fan-out, file and tool-call cost, duplicated metadata, links, and drift may
also matter. No single consideration mechanically determines the boundary.

Granularity is not an eligibility threshold. One function's behavior or rationale,
a typedef location, an include-order rule, or a file/folder role can be a complete
useful leaf, including knowledge otherwise expressed as a code comment. Capture
such answers without inflating them into architecture summaries. Broad architecture
and complete specs also belong; choose boundaries by the question and joint use,
not by a rule that favors either coarse or fine knowledge.

A substantial procedure, interface table, specification, argument, or tightly
coupled sequence can be one good leaf. Canonical orientation and repository spine
leaves are intentional aggregation points: `where/am/i.md` orients, while spec, plan,
state, and next provide cohesive projections of governing or current truth.
