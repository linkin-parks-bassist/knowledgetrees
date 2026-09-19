---
status: "unverified"
scope: "knowledgetrees repository"
source: "Owner command split request, 2026-09-19; tools/kt and CLI tests"
review_when: Recheck when root creation changes.
updated_at: "2026-09-19T23:45:40+10:00"
---
Status: Green

`kt init [ORIENTATION]` creates `.knowledge/` in the current working directory. It creates empty `how/`, `what/`, `where/`, `why/`, `does/`, and `is/` branches plus `where/am/i.md` and empty spec, plan, state, and next leaves. The optional argument is written verbatim as that file's contents; without it the file is empty. It refuses to overwrite an existing root. `kt boot` performs the former fresh-session startup: global procedure, exact local orientation, dictionary, and local proof result.
