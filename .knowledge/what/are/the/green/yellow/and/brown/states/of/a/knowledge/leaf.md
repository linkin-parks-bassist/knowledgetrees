---
status: green
revised_at: "2026-09-21T09:03:52+10:00"
---

Every nonempty leaf has one lifecycle color in front matter as `status: green|yellow|brown`. Proof-free specs, plans, procedures, opinions, and other content that is not mechanically verifiable can be green. A new leaf starts green, and adding or editing a leaf keeps its status. Expired `expires_at` or `expires_every` makes an ordinary leaf yellow. A failed proof, malformed proof, or unsupported metadata makes it brown; brown persists until manual check or complete passing proofs on a `verifiable: true` leaf. Yellow cannot be used before re-verification; brown must be diagnosed and repaired.

Every normal `kt prove` evaluation writes `status` in front matter, and only ever lowers it. `kt renew ADDRESS HASH` (tool `kt_renew`) records `checked_at` after manual review, clears any brown, and re-runs that leaf's own proofs, leaving it green or brown; it is the only manual way up, and proof runs never advance it. `revised_at` records the last content change. Only flat front matter stores lifecycle status. `--no-stamp` remains byte-preserving. Content rewrites keep the status and check time and refresh `revised_at`; only `kt renew` records manual review time. Status and proof writes preserve hardlink identity.

A zero-exit `kt prove` run means only that no brown-level failure was detected
in the selected leaves at that time; yellow warnings may still need review. A green
leaf may have no proofs. Neither a green color nor passing predicates establish
that prose is current, leaves agree, every claim is proof-covered, or predicates
faithfully test their claims.

Agents should add optional expiry metadata to factual knowledge liable to change while leaving durable or non-verifiable knowledge green unless there is a concrete reason for review. `kt prove` prints aggregate counts and brown root-qualified paths; yellow warns without listing paths, and brown fails.

`verifiable: true` is the opt-in exception to conservative whole-leaf verification.
It asserts that the leaf contains only concrete facts and every claim is covered by
its proofs. At least one proof is required. When all proofs actually run and pass,
`kt prove` clears sticky falsification and auto-greens the
leaf. Missing, malformed, skipped, or failing proofs make it brown. Agents must
review coverage before adding the flag because proof execution cannot detect an
unproved sentence.
