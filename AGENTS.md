# Knowledge-tree bootstrap

Follow the canonical knowledge-tree procedure once per fresh agent session. When
the harness supplies it in context, it is already loaded: do not invoke a bootstrap
skill again. Otherwise load `knowledgetrees` as the compatibility fallback.
Perform startup orientation and evidence checks once, not per task or turn.
New question -> `kt` first unless adequately checked knowledge is already loaded;
miss -> determine whether a leaf exists; absent -> investigate and add it (or an
unresolved record) before the next unrelated tool call or completion. The skills
own proof checks, scope, paths, and maintenance. Higher-authority instructions and
permissions always govern.

Keep the roots distinct: `.knowledge/` is this repository's actual operational
knowledge root; `example/` is a public distributable specimen. Do not copy
repository-specific state into `example/` or use the example as a substitute for
project orientation. Validate the example separately with
`kt prove --root example` when changing it.
