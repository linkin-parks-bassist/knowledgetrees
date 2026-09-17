---
status: "unverified"
created_at: "2026-09-17T17:41:48+10:00"
updated_at: "2026-09-17T18:02:12+10:00"
scope: "knowledgetrees repository"
source: "Repository owner lifecycle correction stated 2026-09-17; tools/kt implementation, regression suites, installation, and proof sweeps"
---

Every leaf has exactly one lifecycle state. A leaf with no explicit lifecycle state is green, including specs, plans, procedures, opinions, and other contents that are not actually verifiable. Workflow metadata such as status: unverified or status: unresolved does not make a leaf yellow. A leaf may explicitly store state: green, state: yellow, or state: brown. Yellow means the leaf explicitly declares state: yellow or its optional expiry has elapsed; agents must not rely on its contents until they re-verify it. Brown means the leaf explicitly declares state: brown, has sticky falsified_at metadata, has malformed proof structure, or has a failing proof; agents must diagnose and repair it. Optional expires_at is an ISO 8601 date/time with timezone. Optional expires_every is a duration measured from verified_at and accepts compact or plain-English seconds-through-weeks forms such as 14d, 2 weeks, or two weeks. Agents should optionally add expiry metadata to factual knowledge liable to change, while leaving durable or non-verifiable knowledge green unless there is a concrete reason for review. kt prove always prints green, yellow, and brown totals, prints each non-green leaf as ROOT:relative/path.md, treats yellow as a warning without failing solely for yellow, and returns failure when any leaf is brown.
