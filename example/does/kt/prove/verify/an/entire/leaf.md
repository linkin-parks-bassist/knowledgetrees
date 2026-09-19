---
status: unverified
scope: public knowledge-tree procedure
source: tools/kt; proof-stamp integration tests
review_when: Recheck governing semantics or CLI behavior changes.
---
Status: Green

Only by explicit opt-in. Normally `kt prove` checks marked assertions without
establishing whole-leaf correctness. A leaf declaring `verifiable: true` asserts
that it contains only concrete facts and every claim is proof-covered; if all its
proofs run and pass, the command records whole-leaf verification and auto-greens
it. See [proof verification](../../../../../../how/to/check/knowledgetree/proofs.md).
