#!/usr/bin/env python3
"""Measure CLI wall time on an isolated corpus; optionally compare old output.

python3 tests/benchmark-kt.py --baseline /tmp/old-kt --repeats 5
Not part of the regression glob: timing is evidence, not a flaky pass threshold.
"""
import argparse
import json
import os
from pathlib import Path
import statistics
import subprocess
import sys
import tempfile
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--leaves", type=int, default=512)
    parser.add_argument("--roots", type=int, default=24)
    args = parser.parse_args()
    if min(args.repeats, args.leaves, args.roots) < 1:
        parser.error("counts must be positive")
    current = Path(__file__).resolve().parents[1] / "tools/kt"
    scripts = ([args.baseline.resolve()] if args.baseline else []) + [current]
    with tempfile.TemporaryDirectory(prefix="kt-benchmark-") as temporary:
        base = Path(temporary)
        home = base / "home"
        project = home / "project"
        local = project / ".knowledge"
        global_root = home / ".knowledge"
        roots = [local, global_root] + [
            home / "registered/deep/tree" / str(n) for n in range(args.roots)]
        for root in roots:
            root.mkdir(parents=True)
            (root / "where/am").mkdir(parents=True)
            (root / "where/am/i.md").write_text("Benchmark orientation.\n")
        for n in range(args.leaves):
            path = roots[n % len(roots)] / f"how/to/topic-{n % 16}/answer-{n}.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("---\nstatus: green\n---\n\n"
                            f"Answer {n}: verify the amber compiler.\n\n"
                            "The shared procedure explains verification.\n")
        config = base / "roots.json"
        config.write_text(json.dumps({"roots": {
            f"bench-{n}": {"path": str(root), "access": "allow"}
            for n, root in enumerate(roots)}}))
        # A separate HOME/config/state prevents access to personal knowledge,
        # approvals, session databases, and automatic stale-grant pruning.
        env = {key: value for key, value in os.environ.items()
               if not key.startswith("KT_") and key not in
               ("CODEX_THREAD_ID", "OPENCODE_SESSION_ID")}
        env.update(HOME=str(home), KT_CONFIG=str(config), KT_GLOBAL_ROOT=str(global_root),
                   XDG_STATE_HOME=str(base / "state"), NO_COLOR="1")
        commands = {
            "miss": ["how", "to", "zzyzx-unfindable"],
            "find": ["find", "amber", "compiler"],
            "grep": ["grep", "amber"],
            "dictionary": ["dict"],
            "status": ["status"],
            "exact": ["where", "am", "i"],
        }
        print(f"{args.leaves} leaves, {len(roots)} roots; median of {args.repeats} warm runs")
        for label, command in commands.items():
            samples = [[] for _ in scripts]
            reference = None
            # Warm both versions, then interleave measured calls to reduce order bias.
            for iteration in range(args.repeats + 1):
                for index, script in enumerate(scripts):
                    start = time.perf_counter()
                    result = subprocess.run([sys.executable, str(script), *command],
                                            cwd=project, env=env, capture_output=True,
                                            stdin=subprocess.DEVNULL, timeout=60)
                    elapsed = time.perf_counter() - start
                    expected = 1 if label == "miss" else 0
                    if result.returncode != expected:
                        raise AssertionError(f"{label}: unexpected exit {result.returncode}: "
                                             f"{result.stderr.decode(errors='replace')}")
                    output = (result.returncode, result.stdout, result.stderr)
                    if reference is None:
                        reference = output
                    if output != reference:
                        raise AssertionError(f"{label}: output/exit status changed for {script}")
                    if iteration:
                        samples[index].append(elapsed)
            medians = [statistics.median(sample) for sample in samples]
            times = " -> ".join(f"{value * 1000:.2f} ms" for value in medians)
            speedup = f" ({medians[0] / medians[1]:.2f}x)" if len(medians) == 2 else ""
            print(f"{label:12} {times}{speedup}", flush=True)


if __name__ == "__main__":
    main()
