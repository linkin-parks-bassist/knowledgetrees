---
status: green
revised_at: "2026-09-20T15:15:55+10:00"
---

From this repository directory, run `python3 sync-kt-instructions.py --check` to compare curated source guidance with installed global leaves and skill hardlinks. Run `python3 sync-kt-instructions.py` to refresh them after source guidance changes. The intentionally untracked, Git-excluded script defines its current leaf and skill sets in `LEAVES` and `SKILLS`; do not maintain a separate count here. It renders public example scope as personal global scope like the installer and normalizes successful proof timestamps during comparison.

Replaced content is backed up under `~/.local/state/knowledgetrees/instruction-backups/`. Repository and installed leaves have separate inodes; installed rewrites cannot change public source. Personal leaves, orientations, and project spines are untouched. Executables, hooks, and the MCP server (and its harness registrations) still require installer deployment. The installer removes its former managed home `AGENTS.md` block while preserving unrelated instructions. Updates are manual; refresh after repository guidance changes, then recheck drift and relevant proofs. Restart clients or start fresh sessions to refresh loaded instructions.
