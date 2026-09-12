# Knowledge-tree bootstrap

As the first bootstrap action of a fresh agent session, invoke the `knowledgetrees`
skill and follow its procedures throughout the session without reinvoking per task.
New question -> `kt` first unless adequately checked knowledge is already loaded;
miss -> determine whether a leaf exists; absent -> investigate and add it (or an
unresolved record) before the next unrelated tool call or completion. The skills
own proof checks, scope, paths, and maintenance. Higher-authority instructions and
permissions always govern.

Keep the roots distinct: `.knowledge/` is this repository's actual operational
knowledge root; `example/` is a public distributable specimen. Do not copy
repository-specific state into `example/` or use the example as a substitute for
project orientation. Validate the example separately with
`tools/verify-knowledgetree-proofs --root example` when changing it.
