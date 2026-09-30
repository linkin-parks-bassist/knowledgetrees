---
status: green
revised_at: "2026-09-30T11:20:00+10:00"
---

Event-triggered expiry is a deferred design, not implemented behavior. A leaf could declare repository or system events that make its freshness uncertain—for example, a plan after a commit or a code-dependent answer after relevant source changes. A trigger would request manual whole-leaf review; it would not establish falsity or update `checked_at`.

The design remains unresolved: declaration syntax, watched paths or event identities, reliable detection across Git and non-Git trees, lifecycle transition, missed-hook recovery, and interaction with time-based `expires_at` and `expires_every`. Do not schedule implementation until the owner prioritizes it and these semantics have a specification.
