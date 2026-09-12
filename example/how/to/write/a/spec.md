---
verified_at: '2026-09-12T13:51:10+10:00'
verified_by: codex /root
scope: public knowledge-tree example
source: distilled from Superpowers 6.3.0 brainstorming methodology
verification: Compared the leaf with the quarantined brainstorming skill and retained its reusable specification guidance without mandatory ceremony.
review_when: Recheck when specification practice changes.
---

First establish whether the proposed work is cohesive enough for one specification.
If it spans independent systems, separate them and specify the first useful slice.
Inspect the existing context, then resolve the uncertainties that affect purpose,
constraints, interfaces, success criteria, error behavior, and testing. Ask one
focused clarification at a time when an answer would materially change the design;
prefer concrete choices when the trade-off can be expressed clearly.

Compare plausible approaches and record the selected one with its trade-offs. Write
the specification as current requirements and decisions, not a transcript. Cover the
goal and non-goals, architecture and component responsibilities, interfaces and data
flow, failure handling, acceptance criteria, and verification strategy. Match detail
to risk: a straightforward section can be brief; a consequential interface must be
precise enough that two implementers would build compatible results. Remove
unrequested features and avoid placeholders.

Before treating the specification as ready, scan for incompleteness, internal
contradictions, ambiguous requirements, and scope too broad for one implementation
plan. Resolve substantive findings in the specification itself.
