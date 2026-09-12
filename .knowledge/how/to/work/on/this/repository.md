---
verified_at: '2026-09-12T14:07:43+10:00'
verified_by: codex /root
scope: knowledgetrees repository
source: repository layout and knowledgetrees operating procedure
verification: Confirmed the project root, visible example root, verifier location, and review-before-push boundary.
review_when: Recheck when repository layout or publication workflow changes.
---

Use `.knowledge` for this repository's operational knowledge and `example/` for the
visible distributable corpus. Run `tools/verify-knowledgetree-proofs` for the project
root and `tools/verify-knowledgetree-proofs --root example` for the example. Update
both only when their distinct scopes require it. Do not push until the repository
owner approves the local review commit. Never place repository requirements, work
state, or publication status in `example/`; never use example content as a
substitute for repository orientation.
