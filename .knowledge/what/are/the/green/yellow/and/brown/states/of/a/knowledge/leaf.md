---
status: "unverified"
created_at: "2026-09-17T17:41:48+10:00"
updated_at: "2026-09-18T12:20:42+10:00"
scope: "knowledgetrees repository"
source: "Repository owner lifecycle persistence requirement 2026-09-18; tools/kt implementation and regression tests"
---
Status: Green

Every leaf has one lifecycle color. Missing lifecycle metadata defaults to green, including specs, plans, procedures, opinions, and other contents that are not actually verifiable. Workflow YAML `status: unverified/unresolved` does not determine color. Optional YAML `state: green/yellow/brown` remains an explicit override. Expired `expires_at` or `expires_every` makes a leaf yellow. Sticky `falsified_at`, malformed proofs, or failing proofs make it brown. Yellow cannot be used before re-verification; brown must be diagnosed and repaired.

Every normal `kt prove` evaluation writes the result inside the leaf as `Status: Green`, `Status: Yellow`, or `Status: Brown`, immediately after front matter or at the top of a legacy body-only leaf. This generated body line records the last evaluation but does not drive the next one. Legacy leaves without it remain compatible and default green. `--no-stamp` remains byte-preserving. Content rewrites remove the old generated line because it describes previous contents; the next normal evaluation writes the new result. Status and proof writes preserve hardlink identity.

Agents should add optional expiry metadata to factual knowledge liable to change while leaving durable or non-verifiable knowledge green unless there is a concrete reason for review. `kt prove` prints aggregate counts and every non-green root-qualified path; yellow warns and brown fails.

`verifiable: true` is the opt-in exception to conservative whole-leaf verification.
It asserts that the leaf contains only concrete facts and every claim is covered by
its proofs. At least one proof is required. When all proofs actually run and pass,
`kt prove` records `verified_at`, clears sticky falsification, and auto-greens the
leaf. Missing, malformed, skipped, or failing proofs make it brown. Agents must
review coverage before adding the flag because proof execution cannot detect an
unproved sentence.
