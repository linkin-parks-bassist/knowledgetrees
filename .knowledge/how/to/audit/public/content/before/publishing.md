---
status: green
revised_at: "2026-09-20T16:23:37+10:00"
---

Before pushing, scan every tracked file for material that must not be public, because this repository is published and its own rule is that public leaves contain no private host, customer, or owner-identifying material.

Build the pattern list locally from things that identify the owner and their private work: home-directory paths, the account name, email addresses, and the names of private projects or trees. Do not write those names into any tracked file, including this one; keep them in your shell or a private note. Then run: `git ls-files | xargs grep -n -I -E "PATTERN1|PATTERN2"` and read each hit in context. Scan `tests/` separately, since fixtures should be synthetic temp paths, and check that `git status` shows no untracked file that `git add -A` would sweep in.

Fix a hit at HEAD by rewriting the owning leaf with `kt rewrite` (for example `~` instead of a home path, or "a private project tree" instead of a name). Removing it from HEAD does not remove it from earlier commits: anything already pushed stays in history, and cleaning that needs a history rewrite and force-push, which requires the owner's explicit instruction. Tell the owner what remains in history.

Evidence: the 2026-09-20 scan found a private project name and a home-directory path in `what/is/the/state.md`. The name arrived when another session's in-session note was merged into a leaf during staging, and the path predated the session; both were already pushed, so only HEAD was fixed. Notes written mid-session about private trees are the usual source, so scan after merging them.
