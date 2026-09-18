---
status: "unverified"
source: "tools/kt-hooks bootstrap_context; tools/kt init; tests/test-hooks.py; tests/test-opencode-hooks.mjs"
review_when: Recheck startup interfaces, init output, or hook lifecycle rules.
updated_at: "2026-09-18T12:09:02+10:00"
---

Codex SessionStart and OpenCode system-context startup inject only a compact instruction to run `kt init` once. Hooks read or inject no leaf bodies. The agent-run command prints the canonical global procedure and exact current-working-directory local orientation, then the accessible dictionary, then the local proof result. It does not preload spine or task-specific leaves and never searches parent directories for orientation.

Codex startup/resume/clear/compact events and OpenCode system-context assembly retain the once-per-fresh-session instruction. Resume and compaction preserve completed initialization and rerun only when it was genuinely lost or exact local scope changed. OpenCode still requires restart after installed plugin changes.

Failure-triggered lookup/capture reminders and Stop/idle capture-review bookkeeping remain separate and unchanged. Hooks perform no model calls, run no proofs, and grant no execution or access authority.
