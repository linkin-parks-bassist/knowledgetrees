---
status: "unverified"
scope: public knowledge-tree example
source: "tools/kt dictionary integration tests; fresh Codex SDL2 installation trace supplied by owner, 2026-09-15"
review_when: Recheck when leaf path rules, root access, kt dict, or live discovery behavior changes.
updated_at: "2026-09-15T18:06:14+10:00"
---

A knowledge-tree dictionary is the sorted set of useful unique path segments
appearing in Markdown leaf paths across selected accessible roots. `kt dict` prints
a single comma-separated line, removes the final `.md`, preserves hyphenated
components, and prints repeated segments only once. It omits segments of two
characters or fewer and standard grammatical or navigation words such as `a`,
`to`, `how`, `when`, `what`, and `where`. It reads no leaf bodies and emits no full
leaf paths.

With no arguments, `kt dict` includes every root currently accessible to kt. Root
labels or configured canonical root paths restrict the command, for example
`kt dict local global`. Normal access and force-private rules apply, including to
registered restricted subtrees inside an allowed root.

The once-per-session bootstrap runs `kt dict` once. This gives a fresh agent a
compact vocabulary for later semantic queries without loading unrelated answers or
a complete tree listing. Dictionary membership indicates only that a segment occurs
somewhere; it does not reveal a path, establish that a particular leaf exists, or
replace kt lookup, full reads, evidence review, and proof checks.

In one live check, a fresh Codex session was asked to install SDL2. It began with
`kt dict`, queried `what is the package manager` and `how to install packages`, then
opened `global:how/to/install/packages.md` and
`global:how/to/obtain/sudo-authorization.md` before running the local proof check.
It therefore found the intended authorization procedure instead of trying `sudo -n`.
This demonstrates the complete intended discovery path in one session; it does not
establish a general success rate. The same observation
showed that domain-specific global segments increase startup output, motivating
separate restricted domain roots for knowledge such as Vivado/Vitis procedures.
