---
status: green
revised_at: "2026-09-20T10:28:29+10:00"
---

A passing `kt prove` run means the selected leaves showed no failure detectable
by the verifier at that time. It checks metadata, expiry, proof structure, and
marked predicates; even proof-free leaves can be green. It cannot establish that
prose is current, that leaves agree, or that every claim has a proof.

Normally it does not verify a whole leaf. `verifiable: true` is an author-reviewed
assertion that the leaf contains only concrete facts and eligible proofs cover
every claim. If all proofs pass, `kt prove` auto-greens that leaf, conditional on
that coverage assertion and the predicates actually testing the claims. It cannot
independently validate either condition. See [proof verification](../../../../../../how/to/check/knowledgetree/proofs.md).
