---
status: "unverified"
created_at: "2026-09-14T22:46:04+10:00"
scope: "local"
source: "Manual refresh expanded to definition and atomicity guidance, 2026-09-14"
updated_at: "2026-09-14T22:50:13+10:00"
---
Status: Green

From this repository directory, run python3 sync-kt-instructions.py after changing or pulling core kt guidance. This intentionally untracked, Git-excluded local script force-refreshes fourteen curated core instruction leaves from example/ into the installed global tree, rendering public example scope as personal global scope just like the installer, and relinks both harnesses five skill entry points to their installed canonical leaves. Use --check to detect drift without writes. Successful proof timestamp refreshes
are normalized during comparison, so they do not appear as guidance drift. Replaced content is backed up under ~/.local/state/knowledgetrees/instruction-backups/. The repository and installed leaves no longer share inodes, so installed rewrites cannot change public source. Personal leaves, orientations and project spines are untouched. Executables and hooks still require installer deployment. Updates are manual, not automatic; run the script when repo guidance changes. Restart clients or start fresh sessions to refresh loaded instructions.
