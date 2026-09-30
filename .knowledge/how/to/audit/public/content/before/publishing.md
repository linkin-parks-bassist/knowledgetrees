---
status: green
revised_at: "2026-09-30T11:20:00+10:00"
---

Before pushing, scan every tracked file for material that must not be public. This repository is published, and public leaves must not contain private host, customer, account, or owner-identifying material.

Build the pattern list locally from private identifiers: home-directory paths, account and email identities, and names of private projects or trees. Never write those identifiers into tracked guidance. Search tracked files, read every hit in context, scan test fixtures separately, and inspect untracked files that staging could accidentally include.

Replace private identifiers in current content with truthful generic forms such as `~` or “a private project tree.” Removing a value from HEAD does not remove it from published Git history; a history rewrite and force-push require the owner's explicit instruction. If a sensitive value remains in history, report that fact without repeating the value unnecessarily.

Run this audit after all tree reconciliation and merges, immediately before publication. Mid-session notes and copied private-tree evidence are common ingress paths, so a prior clean scan is not sufficient.
