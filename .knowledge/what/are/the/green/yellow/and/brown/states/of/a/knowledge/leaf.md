---
status: green
revised_at: "2026-09-20T09:26:15+10:00"
---

Every leaf has one lifecycle color in front matter as `status: green|yellow|brown`. Proof-free specs, plans, procedures, opinions, and other content that is not mechanically verifiable can be green. A new or revised leaf starts yellow. Expired `expires_at` or `expires_every` makes a leaf yellow. A failed proof, malformed proof, or unsupported metadata makes it brown; brown persists until manual check or complete passing proofs on a `verifiable: true` leaf. Yellow cannot be used before re-verification; brown must be diagnosed and repaired.

Every normal `kt prove` evaluation writes `status` in front matter. `kt check ADDRESS HASH` records `checked_at` after manual review; proof runs never advance it. `revised_at` records the last content change. Only flat front matter stores lifecycle status. `--no-stamp` remains byte-preserving. Content rewrites set yellow until the next check. Status and proof writes preserve hardlink identity.

Agents should add optional expiry metadata to factual knowledge liable to change while leaving durable or non-verifiable knowledge green unless there is a concrete reason for review. `kt prove` prints aggregate counts and brown root-qualified paths; yellow warns without listing paths, and brown fails.

`verifiable: true` is the opt-in exception to conservative whole-leaf verification.
It asserts that the leaf contains only concrete facts and every claim is covered by
its proofs. At least one proof is required. When all proofs actually run and pass,
`kt prove` clears sticky falsification and auto-greens the
leaf. Missing, malformed, skipped, or failing proofs make it brown. Agents must
review coverage before adding the flag because proof execution cannot detect an
unproved sentence.
