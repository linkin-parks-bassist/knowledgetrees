---
status: "unverified"
source: "tools/kt-hooks bootstrap_context; tests/test-hooks.py; final privacy implementation"
review_when: Recheck startup interfaces or root discovery rules.
updated_at: "2026-09-13T13:51:54+10:00"
---

Codex SessionStart and OpenCode system-context bootstrap share the Python startup
loader. It resolves the supplied cwd and reads only that directory’s
.knowledge; it never searches parent directories. It appends where/am/i.md verbatim after the canonical procedure,
labeling the source and retaining the obligation to verify evidence/proofs.
It never substitutes a parent or global orientation when the local file is missing;
missing or oversized (over 64 KiB) orientation reports a diagnostic and retains
the canonical bootstrap. No root means no injected project orientation.
Codex startup/resume/clear/compact events use the same loader; OpenCode loads it
at plugin startup and retains a single block in rebuilt system context.
OpenCode still requires restart after installed plugin/context changes.

Both harnesses share diagnostic failure detection and Stop/idle bookkeeping.
OpenCode tests cover metadata-free diagnostics through tool.execute.after and
terminal tool-part events, explicit exit-zero precedence, and existing one-shot
review/session isolation. No command wrapping or uncertainty scanner is added.
Source: tools/kt-hooks; tools/kt-opencode.mjs; tests/test-hooks.py;
tests/test-opencode-hooks.mjs. Relevant integration checks passed.

Privacy boundary: automatic orientation injection is restricted to the supplied
session directory. Parent/home orientations are never searched or used as fallback.
The canonical global procedure is injected only when its root is not force-private
outside exact local scope. The shared loader checks current root policy before
reading it; bypass cannot override force-private. When permitted, it does not
inject global orientation.
