---
status: "unverified"
source: "tools/kt-hooks bootstrap_context; tools/kt init; tests/test-hooks.py; tests/test-opencode-hooks.mjs"
review_when: Recheck startup interfaces, init output, or hook lifecycle rules.
updated_at: "2026-09-18T12:02:33+10:00"
---

Codex SessionStart and OpenCode system-context startup inject only a compact instruction to run `kt init` once. Hooks no longer read or inject the canonical procedure, project orientation, or any other leaf body. The agent-run command uses the canonical global procedure and exact current-working-directory local root; it prints the global procedure and local orientation/spec/plan/state/next leaves, then the accessible dictionary, then the local proof result. It never searches parent directories for orientation.

Codex startup/resume/clear/compact events and OpenCode system-context assembly retain the once-per-fresh-session instruction. Resume and compaction preserve completed initialization and rerun only when it was genuinely lost or exact local scope changed. OpenCode still requires restart after installed plugin changes.

Failure-triggered lookup/capture reminders and Stop/idle capture-review bookkeeping remain separate and unchanged. Hooks perform no model calls, run no proofs, and grant no execution or access authority.
