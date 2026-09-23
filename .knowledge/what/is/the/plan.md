---
status: green
revised_at: "2026-09-24T08:10:00+10:00"
---

Keep the CLI, README, public `example/` guidance, installed global guidance,
and operational `.knowledge/` aligned with the flat leaf metadata contract.

For each change:

1. Repair any known stale or contradictory active knowledge first. Locate its
   owner, check current evidence, and preserve still-valid content.
2. Change the CLI and focused regression coverage together.
3. Build an affected-owner inventory covering narrow and central procedures, policy/access guidance, spec/plan/state/next, README and CLI help, startup payloads, public example, generated surfaces, and installed guidance. Search positively for the new behavior and negatively for superseded counts, lists, fallbacks, and limitations; read every hit in context and repair all owners. Only then run the Python and OpenCode suites plus `git diff --check`.
4. Run `kt prove --no-stamp` across affected roots. Inspect brown leaves and
   manually review expired yellow leaves before relying on them.
5. Preview installation, install authorized changes, refresh curated instruction
   copies, and check installed bytes and proof results.
6. Update current state and next action, then publish under the user’s current authorization, including earlier in-scope instructions.

Keep repository-specific knowledge in `.knowledge/`, the public example generic,
and the example orientation empty. Preserve access policy and archived trees.
