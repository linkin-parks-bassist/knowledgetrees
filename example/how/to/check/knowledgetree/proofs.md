---
status: unverified
scope: public knowledge-tree procedure
source: tools/kt; tools/verify-knowledgetree-proofs; tests/test-kt.py; tests/test-proof-stamps.py
review_when: Recheck proof engine, compatibility entry point, or access enforcement changes.
---

Use `kt prove` to check marked proofs. Verification is built into kt; it does
not launch or require a separately installed verifier. From a directory containing
an accessible `.knowledge` root:

```bash
kt prove
kt prove vivado
kt prove --root /path/to/approved/.knowledge --no-stamp
```

Before installation, use `tools/kt prove` from the checkout. Root access checks
apply before proof execution, including restrictions on registered nested trees.
`kt prove --help` lists verification options without requiring root access.

The old `verify-knowledgetree-proofs` executable is a small compatibility entry
point into the same kt proof engine, not another implementation. It preserves
legacy standalone root selection, which does not enforce kt access policies;
new agent and harness integrations should use `kt prove`. Existing standalone
scripts continue to work when the compatibility entry point and kt are together.

Each positional token must match an exact directory component or filename stem;
multiple tokens select their disjunction. Use `-r PATH` or `--root PATH` to select a
knowledge root explicitly when invoking it elsewhere; positional tokens following
that option retain the same exact, disjunctive semantics.

Normal success is quiet and returns 0. Every failure returns 1 and prints the
deduplicated failing leaf paths to standard error, regardless of verbosity. Use `-v`
or `--verbose` when diagnostic output is needed; verbose mode additionally lists
every selected leaf, proof result, error, and summary in the former detailed format.
The verifier runs only scripts explicitly introduced by
`Proof:`, checks that tree payload files are Markdown leaves, and treats discovery,
structure, timeout, or proof failures as failure. A semantic filter matching no
leaves succeeds as an empty check. Proofs run from the directory containing
`.knowledge`, with a ten-second default timeout per proof.

Write new markers as `Proof: (verified at _)`. Every successful proof execution
replaces the placeholder or previous timestamp with ISO 8601 local time including
timezone. Failed proofs receive `Proof: (falsified at …)`, and a failing proof or
malformed proof structure sets leaf-level `falsified_at` metadata. Bare `Proof:`
remains compatible; both verified and falsified markers are rechecked on later runs.
Write failures or concurrent content changes
make verification fail rather than silently losing an update.

Only proof markers are refreshed. Leaf-level `verified_at` records an independent
whole-leaf review and is not changed by the verifier. Use `--no-stamp` to execute
proofs without writing markers. Timestamp writes preserve existing hardlinks.

Leaf falsification is sticky and makes checks fail until an agent independently
reviews and repairs the leaf and explicitly clears `falsified_at`. Passing every
proof is necessary but not sufficient for leaf validation; the verifier never
promotes the whole leaf to verified or repairs its knowledge automatically.
