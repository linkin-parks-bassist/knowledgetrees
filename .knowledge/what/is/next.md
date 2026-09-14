---
status: "unverified"
scope: knowledgetrees repository
source: "Authorized Projects parent-folder relocation and focused verification 2026-09-14"
review_when: Update after validation, deployment, or publication.
updated_at: "2026-09-14T23:12:16+10:00"
---

After changing or pulling core kt guidance, run python3 sync-kt-instructions.py
from this repository. Use --check to audit drift. Start a fresh agent session to
assess the refreshed interface instructions. See
how/to/update/installed/kt/instructions.md for the manual local workflow.

No repository repair remains for the parent-folder rename. Use the canonical new checkout path for new sessions.

The owner authorized publication and installation of the inline rewrite and
local-startup changes. Installer deployment and instruction refresh are complete;
no implementation or installation work remains. Fresh sessions pick up refreshed
instructions.

Keep deprecated kt amend available until the living legacy workers have finished;
removal requires a later decision. New work uses kt rewrite.
