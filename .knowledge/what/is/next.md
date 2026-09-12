---
verified_at: '2026-09-12T12:21:21+00:00'
verified_by: codex /root
scope: knowledgetrees repository
source: completed publication plan and current repository state
verification: Checked adapter installation, OpenCode discovery, Codex hook-trust requirements, isolated tests, and the publication approval boundary; behavioral compliance remains unverified.
review_when: Update whenever the next actionable step changes.
---

Review the hook implementation commit and approve publication. Locally, review
and trust the new Codex PreToolUse definition using `/hooks`, then test plain false
to verify automatic wrapping. The post-tool reminder has been delivered live for
wrapped false. Restart OpenCode to load its discovered
plugin, and start a new Copilot CLI session. Failure reminders and one-shot task-end
capture review are implemented; isolated adapter tests do not establish actual model
adoption or guarantee that knowledge was captured. Do not publish before approval.

When model capacity is available, evaluate kt-first lookup and miss-resolution behavior with an ordinary
task relying only on installed harness instructions, without prompting knowledge
retrieval or naming the expected answer paths. This is not mechanically proved by
installer tests or skill discovery.
