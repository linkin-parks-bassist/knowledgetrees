---
status: green
revised_at: "2026-09-20T14:54:10+10:00"
---

The home and repository AGENTS bootstraps have been removed. The installer now removes its legacy home block without recreating it; all three supported CLI startup paths use hooks. No further AGENTS migration work is pending. The event-triggered expiry idea remains deferred as requested. Keep the two pre-existing OpenCode hook edits separate and repair any newly discovered stale active leaf before reliance.
