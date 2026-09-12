---
verified_at: '2026-09-12T14:22:23+10:00'
verified_by: codex /root
scope: public knowledge-tree example
source: sanitized adaptation of the canonical global knowledge-tree methodology
verification: Compared the generic answer with the verifier implementation and exercised its installed location in the installer integration test.
review_when: Recheck when the knowledge-tree model or operating procedure changes.
---

Install the independent knowledge-tree proof verifier at
`~/.knowledge/.tools/verify-knowledgetree-proofs`. From this repository before
installation, use the packaged source at `tools/verify-knowledgetree-proofs`.

From a directory containing `.knowledge`, check every marked proof in it with:

```bash
~/.knowledge/.tools/verify-knowledgetree-proofs
```

To check only leaves whose relative semantic path contains an exact `vivado`
component, run:

```bash
~/.knowledge/.tools/verify-knowledgetree-proofs vivado
```

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

For a user-wide installation, keep one executable copy at
`~/.knowledge/.tools/verify-knowledgetree-proofs`. Harness integrations should call
that canonical installed copy rather than multiplying it per harness.
