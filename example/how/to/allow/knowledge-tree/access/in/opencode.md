---
verified_at: '2026-09-12T16:50:03+10:00'
verified_by: codex /root
scope: public knowledge-tree example
source: https://opencode.ai/docs/permissions/; installer implementation and integration checks
verification: Reviewed scoped permission merging and consent-before-write behavior.
review_when: Recheck after OpenCode permission semantics or installer policy changes.
---

Grant knowledge-tree access only after informed consent. Read contents may reach
the configured model provider. The installer asks `[n/Y]` before any writes;
declining or noninteractive EOF cancels installation.

OpenCode needs both `read` and `external_directory` permission for an outside
workspace tree. Allow these for the absolute home-expanded `.knowledge/**` and
`.agents/**` paths. Allow `edit` for `.knowledge/**`; keep `.agents/**` edits
at `ask`. Enable only the `knowledgetrees` skill without changing other skills.
Preserve unrelated settings and permission defaults. Last matching rules win,
so append the scoped grants after existing broad rules.

Review [OpenCode's permission documentation](https://opencode.ai/docs/permissions/)
when its semantics change. A tool permission is not authorization for unrelated
actions, privilege escalation, or publication of private knowledge.
