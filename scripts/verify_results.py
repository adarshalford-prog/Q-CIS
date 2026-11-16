#!/usr/bin/env python3
"""Compare a reproduction run against the committed reference output.

    python scripts/verify_results.py

Tolerance policy (documented, and enforced literally below)
-----------------------------------------------------------
The reference implementation is fully deterministic given a seed, so every numeric
column must agree **exactly** in exact arithmetic. Floating-point reduction order is
fixed in the code, but different BLAS builds may reorder some sums, so a small
tolerance is allowed:

    accuracies and cross-validated features : 1e-6 absolute
    final_loss                              : 1e-6 absolute
    integer counts (n_states, n_params)     : exact

``fit_seconds`` is wall-clock timing and is **excluded** from the comparison.

Exit code is 0 when everything is within tolerance, 1 otherwise.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KEY = ("family", "mechanism", "seed")
FLOAT_COLS = ("train_accuracy", "test_accuracy", "final_loss",
              "cv_linear", "cv_nonlinear", "cv_gap", "cv_1nn", "fisher_ratio")
INT_COLS = ("n_states", "n_params", "n_train", "n_test")
TOL = 1e-6


def load(path):
    with open(path, encoding="utf-8") as f:
        return {(r["family"], r["mechanism"], r["seed"]): r for r in csv.DictReader(f)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--actual", default=os.path.join(ROOT, "results/raw/fits.csv"))
    ap.add_argument("--reference", default=os.path.join(ROOT, "results/reference/reference_fits.csv"))
    ap.add_argument("--tol", type=float, default=TOL)
    args = ap.parse_args(argv)

    if not os.path.exists(args.actual):
        print(f"missing actual results: {args.actual}\n"
              f"run: python scripts/run_reproduction.py --all", file=sys.stderr)
        return 1
    if not os.path.exists(args.reference):
        print(f"missing reference results: {args.reference}", file=sys.stderr)
        return 1

    act, ref = load(args.actual), load(args.reference)
    problems = []

    missing = sorted(set(ref) - set(act))
    extra = sorted(set(act) - set(ref))
    for k in missing[:10]:
        problems.append(f"missing row {k}")
    for k in extra[:10]:
        problems.append(f"unexpected row {k}")

    compared = 0
    for k in sorted(set(ref) & set(act)):
        a, r = act[k], ref[k]
        for col in FLOAT_COLS:
            av, rv = a.get(col, ""), r.get(col, "")
            if av == "" or rv == "":
                continue
            av, rv = float(av), float(rv)
            if (av != av) and (rv != rv):      # both NaN
                continue
            if abs(av - rv) > args.tol:
                problems.append(f"{k} {col}: actual {av!r} vs reference {rv!r}")
        for col in INT_COLS:
            if a.get(col, "") != r.get(col, ""):
                problems.append(f"{k} {col}: actual {a.get(col)} vs reference {r.get(col)}")
        compared += 1

    print(f"compared {compared} rows against {os.path.basename(args.reference)} "
          f"(tolerance {args.tol:g})")
    if problems:
        print(f"\nFAIL: {len(problems)} discrepancies", file=sys.stderr)
        for p in problems[:25]:
            print("  " + p, file=sys.stderr)
        return 1
    print("PASS: reproduction matches the reference output within tolerance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
