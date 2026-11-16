#!/usr/bin/env python3
"""One-command reproduction of this release's reference results.

    python -m pip install -r requirements.txt
    python scripts/run_reproduction.py --all

What it does
------------
1. generates the documented synthetic families from fixed seeds;
2. runs every mechanism in the ablation grid across all families and seeds;
3. runs the classical baselines;
4. computes the family-level statistical audit;
5. writes machine-readable CSV/JSON and a human-readable Markdown summary.

What it does NOT do
-------------------
It does not reproduce the historical Phase 1-7 figures reported in
``RESULTS_SUMMARY.md``. The original experiment code, raw fit-level data and
configurations were never published, so those figures remain author-reported and
cannot be re-executed from this repository. See ``REPOSITORY_AUDIT.md``.

Outputs go to ``results/raw/`` and ``results/summaries/``. Historical records under
``results/reference/`` are never written by this script.

Exit code is non-zero if any stage fails.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def stage(name, argv):
    print(f"\n=== {name} ===", flush=True)
    t0 = time.time()
    proc = subprocess.run(argv, cwd=ROOT)
    dt = time.time() - t0
    if proc.returncode != 0:
        print(f"FAILED: {name} (exit {proc.returncode}) after {dt:.1f}s", file=sys.stderr)
        return False
    print(f"ok: {name} ({dt:.1f}s)", flush=True)
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all", action="store_true", help="run every stage (default)")
    ap.add_argument("--config", default=os.path.join("experiments", "configs", "default.json"))
    ap.add_argument("--outdir", default="results")
    ap.add_argument("--force", action="store_true", help="overwrite existing raw outputs")
    args = ap.parse_args(argv)

    raw = os.path.join(args.outdir, "raw")
    summ = os.path.join(args.outdir, "summaries")
    fits = os.path.join(raw, "fits.csv")

    py = sys.executable
    ok = stage("benchmark", [py, "experiments/run_benchmark.py",
                             "--config", args.config, "--out", fits] +
               (["--force"] if args.force else []))
    if not ok:
        return 1
    ok = stage("statistical audit", [py, "analysis/audit.py", "--fits", fits, "--outdir", summ])
    if not ok:
        return 1

    print("\n=== results ===")
    print(f"raw fits      : {fits}")
    print(f"audit json    : {os.path.join(summ, 'audit.json')}")
    print(f"summary md    : {os.path.join(summ, 'summary.md')}")
    print("\nCompare against the committed reference output with:")
    print("    python scripts/verify_results.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
