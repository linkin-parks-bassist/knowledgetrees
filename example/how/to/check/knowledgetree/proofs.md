---
status: green
revised_at: "2026-09-24T10:09:45+10:00"
---

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

A zero-exit run means only that the selected leaves had no brown-level failure
detected at that time. Yellow expiry warnings may remain, and a green leaf may
have no proofs at all. The verifier cannot judge whether prose is true or current, whether
leaves contradict each other, or whether a predicate faithfully tests its claim.
Treat the result as a limited negative check, not a correctness certificate.

Every run prints two aligned summary lines, for example:

```text
Leaves: 28 total · 28 green · 0 yellow · 0 brown
Proofs:  1 total ·  1 valid · 0 failed · SUCCESS
```

The proof result is `FAIL` when a leaf is brown or a proof fails. Counts are padded
to the widest value in each corresponding column; the result starts under the
brown count. Brown leaf paths are printed to standard error;
yellow paths are shown on leaf read. Yellow is a warning and does not by itself
change the zero exit status. Brown means the tree is busted: the command returns 1. Use `-v`
or `--verbose` when diagnostic output is needed; verbose mode additionally lists
every selected leaf, proof result, error, and summary in the former detailed format.
Normal evaluation writes `status: green|yellow|brown` in front matter. `kt_renew`
(`kt renew`) records `checked_at` after manual review and re-runs the leaf's own proofs; `revised_at` records the last content edit. Evaluation only lowers a status; a `verifiable: true` leaf whose proofs all pass is the one automatic way up.
The verifier runs only scripts explicitly introduced by
`Proof:`, checks that tree payload files are Markdown leaves, and treats discovery,
structure, timeout, or proof failures as failure. A semantic filter matching no
leaves succeeds as an empty check. Proofs run from the directory containing
`.knowledge`, with a ten-second default timeout per proof.

Write the exact timeless marker `Proof:`. It stores neither an outcome nor a
timestamp and is never rewritten after migration. For compatibility, a writing
`kt prove` accepts legacy `Proof: (verified at …)`, `Proof: (verified at _)`, and
`Proof: (falsified at …)` markers, executes their predicates normally, and silently
normalizes them to `Proof:`. `--no-stamp` accepts the same legacy forms without
changing bytes. Legacy timestamp text is not parsed, validated, or treated as
freshness evidence. Every marked predicate runs on every check. A failing predicate
or malformed proof structure sets `status: brown`; the current command result and
verbose diagnostics report the outcome. Write failures
or concurrent content changes make verification fail rather than silently losing an
update.

The evaluated `status` records the current lifecycle color. Proof markers are
timeless and remain unchanged; `kt prove` never updates manual `checked_at`. Use
`--no-stamp` to execute proofs without writing lifecycle status. Status writes
preserve existing hardlinks.

Every selected leaf has one lifecycle state. Proof-free specs, plans, procedures,
and opinions can be green. For an ordinary leaf, green requires no elapsed expiry, no sticky brown status,
valid proof structure, and passing proofs. A fully proof-covered `verifiable: true`
leaf can also be green after expiry when all proofs pass. Yellow means freshness
review is required:
`expires_at` has passed, or `expires_every` after manual `checked_at` has elapsed. Agents
must not rely on yellow contents until they re-verify them. `expires_at` is ISO 8601
with timezone. `expires_every` accepts durations such as `14d`, `2 weeks`, or
`two weeks`; add or rewrite accepts one expiry option at a time.
Add expiry metadata to facts liable to change; do not
penalize inherently non-verifiable knowledge for lacking whole-leaf verification.

For an unflagged leaf, falsification is sticky and makes checks fail until an agent
independently reviews and repairs it, then uses `kt_renew` to clear
brown status. For an unflagged leaf, passing every proof is necessary but does not establish
whole-leaf correctness. The verifier never repairs its knowledge automatically.
Such falsified, malformed, or proof-failing leaves are brown. Brown is an incident,
not a deferred warning: even at startup with no user task, the agent must first
report the affected leaf prominently, stop all unrelated work, diagnose why the
leaf or proof does not match reality, choose and perform the safest remediation,
and re-check it. If safe remediation cannot be established, the agent asks the user
for guidance. Only explicit user permission to ignore that specific brown status
allows unrelated work to resume; the permission does not validate or green the leaf.

Mark a leaf `verifiable: true` when it contains only concrete facts and its
proofs completely cover every claim, after reviewing that coverage. It requires at least one eligible
proof. When all proofs actually run and pass with valid structure, `kt prove`
writes `status: green` even when the prior status was brown. A missing, malformed, skipped, or failing proof makes the leaf
brown. Use the flag only after reviewing proof coverage; passing code cannot prove
an uncovered sentence.
