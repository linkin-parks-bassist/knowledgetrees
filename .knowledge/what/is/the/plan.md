---
status: green
revised_at: "2026-09-20T10:17:58+10:00"
---

Keep the CLI, README, public `example/` guidance, installed global guidance,
and operational `.knowledge/` aligned with the flat leaf metadata contract.

For each change:

1. Repair any known stale or contradictory active knowledge first. Locate its
   owner, check current evidence, and preserve still-valid content.
2. Change the CLI and focused regression coverage together.
3. Compare behavior and CLI help with affected local/global leaves, README,
   AGENTS source and generated templates, public example, and installed guidance.
   Reconcile the meaning of each claim, then run the Python and OpenCode suites
   plus `git diff --check`.
4. Run `kt prove --no-stamp` across affected roots. Inspect brown leaves and
   manually review expired yellow leaves before relying on them.
5. Preview installation, install authorized changes, refresh curated instruction
   copies, and check installed bytes and proof results.
6. Update current state and next action, then publish within owner authorization.

Keep repository-specific knowledge in `.knowledge/`, the public example generic,
and the example orientation empty. Preserve access policy and archived trees.
