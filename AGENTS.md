# Knowledge-tree bootstrap

As the first move of every task, invoke the `knowledgetrees` skill and follow its
bootstrap, orientation, semantic retrieval, proof, maintenance, and continuous-growth
procedures. Use this repository's `.knowledge` root and the applicable broader root.
Run `tools/verify-knowledgetree-proofs` across the repository knowledge tree at
startup, then use semantic path-component tokens for relevant checks at important
junctions. Knowledge-tree paths are not code identifiers: hyphenate genuinely
multi-word components and never use underscores in them.

Keep the roots distinct: `.knowledge/` is this repository's actual operational
knowledge root; `example/` is a public distributable specimen. Do not copy
repository-specific state into `example/` or use the example as a substitute for
project orientation. Validate the example separately with
`tools/verify-knowledgetree-proofs --root example` when changing it.
