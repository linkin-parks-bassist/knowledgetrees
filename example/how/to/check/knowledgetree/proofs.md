---
status: "unverified"
scope: public knowledge-tree procedure
source: "tools/kt built-in proof engine; installer; owner removal of separate verifier"
review_when: Recheck proof engine or access enforcement changes.
updated_at: "2026-09-13T13:54:30+10:00"
---
Status: Green

Use `kt prove` to check marked proofs. Verification is built into kt; it does
not launch or require a separately installed verifier. Bare `kt prove` checks all accessible roots. Use explicit selectors to narrow it:

```bash
kt prove
kt prove --local
kt prove --global vivado
kt prove --root /path/to/approved/.knowledge --no-stamp
```

Before installation, use `tools/kt prove` from the checkout. Root access checks
apply before proof execution, including restrictions on registered nested trees.
`kt prove --help` lists verification options without requiring root access.


Each positional token must match an exact directory component or filename stem;
multiple tokens select their disjunction. Use `--local` for the exact current-directory tree, `--global` for the global
tree, or `-r PATH`/`--root PATH` for another exact accessible root; positional tokens following
that option retain the same exact, disjunctive semantics.

Every run prints one aggregate `green=N yellow=N brown=N` line. Each yellow or
brown leaf is also printed to standard error as `STATE ROOT:relative/path.md`.
Yellow is a warning and does not by itself change the zero exit status. Brown
means the tree is busted: the command returns 1. Use `-v`
or `--verbose` when diagnostic output is needed; verbose mode additionally lists
every selected leaf, proof result, error, and summary in the former detailed format.
Normal evaluation also writes `Status: Green`, `Status: Yellow`, or `Status: Brown`
as a body line immediately after front matter. It is distinct from YAML workflow
`status:` and explicit lifecycle `state:`.
The verifier runs only scripts explicitly introduced by
`Proof:`, checks that tree payload files are Markdown leaves, and treats discovery,
structure, timeout, or proof failures as failure. A semantic filter matching no
leaves succeeds as an empty check. Proofs run from the directory containing
`.knowledge`, with a ten-second default timeout per proof.

Write new markers as `Proof: (verified at _)`. Successful proofs refresh their ISO
8601 check times only on leaves with `expires_at` or `expires_every`; non-expiring
leaves retain existing passing markers unchanged. Failed proofs receive
`Proof: (falsified at …)`, and a failing proof or malformed proof structure sets
sticky leaf-level `falsified_at` once without repeatedly changing its timestamp.
When a repaired non-expiring proof transitions from falsified to passing, its marker
returns to `Proof: (verified at _)` without inventing recurring timestamp churn.
Bare markers remain compatible and every proof is still executed on every check.
Write failures or concurrent content changes
make verification fail rather than silently losing an update.

Proof markers are updated only for expiry refreshes or outcome transitions. The
evaluated `Status:` line is written only when absent or changed. Leaf-level
`verified_at` normally records an independent whole-leaf review; the verifier
adds it on the first successful `verifiable: true` check and refreshes it on later
checks only when the leaf has expiry metadata. Use `--no-stamp` to
execute proofs without writing markers, verification/falsification metadata, or
lifecycle status. Writes preserve existing hardlinks.

Every selected leaf has one lifecycle state. A missing `state` defaults to green,
including for specs, plans, procedures, opinions, and other non-verifiable contents.
Green also requires no elapsed expiry, no sticky falsification, valid proof structure,
and passing proofs. Yellow means re-verification is required: the leaf declares
`state: yellow`, `expires_at` has passed, or its `expires_every` duration after `verified_at` has elapsed. Agents
must not rely on yellow contents until they re-verify them. `expires_at` is ISO 8601
with timezone. `expires_every` accepts durations such as `14d`, `2 weeks`, or
`two weeks`; when both forms exist, the earlier expiry wins.
Use `state: green`, `state: yellow`, or `state: brown` only when an explicit stored
classification is useful. Add expiry metadata to facts liable to change; do not
penalize inherently non-verifiable knowledge for lacking whole-leaf verification.

Leaf falsification is sticky and makes checks fail until an agent independently
reviews and repairs the leaf and explicitly clears `falsified_at`. Passing every
proof is necessary but not sufficient for leaf validation; the verifier never
promotes the whole leaf to verified or repairs its knowledge automatically.
Such falsified, malformed, or proof-failing leaves are brown. An agent encountering
one must diagnose and repair it rather than use or ignore it.

Exception: `verifiable: true` declares that the leaf contains only concrete facts
and that its proofs completely cover every claim. It requires at least one eligible
proof. When all proofs actually run and pass with valid structure, `kt prove`
records whole-leaf `verified_at`, clears sticky `falsified_at`, and writes
`Status: Green`. A missing, malformed, skipped, or failing proof makes the leaf
brown. Use the flag only after reviewing proof coverage; passing code cannot prove
an uncovered sentence.
