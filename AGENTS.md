# Knowledge-tree bootstrap

Follow the canonical knowledge-tree procedure once per fresh agent session. When
the harness supplies it in context, it is already loaded: do not invoke a bootstrap
skill again. Otherwise load `knowledgetrees` as the compatibility fallback.
Perform startup orientation and evidence checks once, not per task or turn. The startup hook injects the complete `kt boot` output. Consume it through its final proof summary. If the hook is unavailable, run `kt boot` directly and consume its complete output without truncation. Diagnose a failed boot before relying on the tree.
New question -> `kt` first unless adequately checked knowledge is already loaded;
miss -> determine whether a leaf exists; absent -> investigate and add it (or an
unresolved record) before the next unrelated tool call or completion. The skills
own proof checks, scope, paths, and maintenance. Higher-authority instructions and
permissions always govern.

Known stale or contradictory active knowledge takes priority over ordinary work.
Stop relying on it; repair the owning leaf and affected guidance before completion.
A green status or passing proof does not certify unproved prose.

Full leaf reads supply a revision hash; edit with `kt rewrite ADDRESS HASH BODY`
and preserve still-valid knowledge already in context.

Keep the roots distinct: `.knowledge/` is this repository's actual operational
knowledge root; `example/` is a public distributable specimen. Do not copy
repository-specific state into `example/` or use the example as a substitute for
project orientation. Validate the example separately with
`kt prove --root example` when changing it.
