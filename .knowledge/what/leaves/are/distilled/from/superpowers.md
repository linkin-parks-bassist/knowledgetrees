---
status: green
revised_at: "2026-09-20T08:51:45+10:00"
---

Exactly four example leaves identify Superpowers as their source.

Proof: (verified at _)

```bash
test "$(grep -rl 'Adapted from Superpowers 6.3.0' example --include='*.md' | wc -l)" = 4
```

These leaves distill the Superpowers 6.3.0 methodology: `how/to/make/a/plan.md`
(from writing-plans), `how/to/write/a/spec.md` (from brainstorming),
`how/to/update/a/spec.md` (from brainstorming and spec-review), and
`when/to/ask/clarification.md` (from the clarification workflow). Each leaf names its Superpowers origin in the answer body. `how/to/install/knowledgetrees.md`
is not Superpowers-derived; it documents this repository's installer.
