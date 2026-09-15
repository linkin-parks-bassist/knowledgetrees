---
scope: knowledgetrees repository
source: "tools/kt built-in proof engine; installer; owner removal of separate verifier"
review_when: Recheck when repository layout or publication workflow changes.
status: "unverified"
updated_at: "2026-09-13T13:54:30+10:00"
---

Use `.knowledge` for this repository's operational knowledge and `example/` for the
visible distributable corpus. Run `kt prove --local` for the project root and `kt prove --root example` for the example. Update
both only when their distinct scopes require it. Publish only within the repository
owner’s authorization. The current session explicitly authorized the completed
CLI changes and their documentation; do not infer authorization for future work. Never place repository requirements, work
state, or publication status in `example/`; never use example content as a
substitute for repository orientation.
