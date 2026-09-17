---
status: "unverified"
created_at: "2026-09-17T17:41:48+10:00"
updated_at: "2026-09-17T17:51:53+10:00"
scope: "knowledgetrees repository"
source: "Repository owner requirement stated 2026-09-17; tools/kt implementation, regression suites, installation, and local/example/global proof sweeps"
---

Every leaf has exactly one derived lifecycle state. Green means the whole leaf has been independently verified, is not expired, has no sticky falsification, and all executable proofs pass. Yellow means the leaf requires verification: it is unverified or its optional expiry has elapsed; agents must not rely on its contents until they re-verify it. Brown means the leaf is falsified because it has sticky falsified_at metadata, malformed proof structure, or a proof fails; agents must diagnose and repair it. Optional expires_at is an ISO 8601 date/time with timezone. Optional expires_every is a duration measured from verified_at and accepts compact or plain-English seconds-through-weeks forms such as 14d, 2 weeks, or two weeks. kt prove always prints green, yellow, and brown totals, prints each non-green leaf as ROOT:relative/path.md, treats yellow as a warning without failing solely for yellow, and returns failure when any leaf is brown.
