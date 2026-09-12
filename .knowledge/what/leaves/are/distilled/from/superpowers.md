---
verified_at: '2026-09-12T15:16:38+10:00'
verified_by: opencode /root
scope: knowledgetrees repository
source: example leaf metadata source lines; README methodology provenance section
verification: Read each example leaf's metadata and the README provenance note; confirmed the four Superpowers-distilled leaves and that how/to/install/knowledgetrees.md derives from the repository installer instead.
review_when: Recheck when the example corpus or its provenance changes.
---

Exactly four example leaves identify Superpowers as their source.

Proof: (verified at 2026-09-12T15:34:29+10:00)

```bash
test "$(grep -rl 'source: distilled from Superpowers' example --include='*.md' | wc -l)" = 4
```

These leaves distill the Superpowers 6.3.0 methodology: `how/to/make/a/plan.md`
(from writing-plans), `how/to/write/a/spec.md` (from brainstorming),
`how/to/update/a/spec.md` (from brainstorming and spec-review), and
`when/to/ask/clarification.md` (from the clarification workflow). Each leaf's
`source:` metadata names its Superpowers origin. `how/to/install/knowledgetrees.md`
is not Superpowers-derived; it documents this repository's installer.
