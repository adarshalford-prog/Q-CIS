#!/usr/bin/env python3
"""Run the Q-CIS mechanism benchmark over the documented synthetic families.

Writes one row per fit to a CSV. Nothing is overwritten in place: the output path is
given explicitly and the script refuses to clobber an existing file unless --force.

Usage
-----
    python experiments/run_benchmark.py --config experiments/configs/default.json \
        --out results/raw/fits.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import platform
import sys
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, ROOT)

from datasets.generation.synthetic import FAMILIES, make, stratified_split  # noqa: E402
from qcis.baselines import BASELINES  # noqa: E402
from qcis.features import geometry_features  # noqa: E402
from qcis.model import QCISClassifier  # noqa: E402

FIELDS = [
    "family", "mechanism", "seed", "n_train", "n_test",
    "train_accuracy", "test_accuracy", "n_states", "n_params",
    "fit_seconds", "final_loss",
    "cv_linear", "cv_nonlinear", "cv_gap", "cv_1nn", "fisher_ratio",
]


def run(config, out_path, force=False, quiet=False):
    if os.path.exists(out_path) and not force:
        raise SystemExit(
            f"refusing to overwrite {out_path} (pass --force to replace it); "
            "historical records are never overwritten by this script"
        )

    base = int(config["base_seed"])
    model_cfg = config["model"]
    test_frac = config["split"]["test_frac"]
    n_splits = config["cv"]["n_splits"]

    rows = []
    t_all = time.time()

    for fam in config["families"]:
        if fam not in FAMILIES:
            raise SystemExit(f"unknown family {fam!r}")
        X, y = make(fam, seed=base)
        tr, te = stratified_split(y, test_frac=test_frac, seed=base)
        Xtr, ytr, Xte, yte = X[tr], y[tr], X[te], y[te]

        # geometry features: training split only
        geo = geometry_features(Xtr, ytr, n_splits=n_splits, seed=base)

        for mech in config["mechanisms"]:
            for seed in config["seeds"]:
                t0 = time.time()
                clf = QCISClassifier(
                    mechanism=mech,
                    n_states_per_class=model_cfg["n_states_per_class"],
                    dim=model_cfg["dim"],
                )
                clf.fit(Xtr, ytr, epochs=model_cfg["epochs"], lr=model_cfg["lr"], seed=seed)
                dt = time.time() - t0
                rows.append({
                    "family": fam, "mechanism": mech, "seed": seed,
                    "n_train": len(ytr), "n_test": len(yte),
                    "train_accuracy": clf.score(Xtr, ytr),
                    "test_accuracy": clf.score(Xte, yte),
                    "n_states": clf.n_states,
                    "n_params": clf.n_trainable_parameters,
                    "fit_seconds": round(dt, 4),
                    "final_loss": float(clf.history_[-1]),
                    **{k: geo[k] for k in
                       ("cv_linear", "cv_nonlinear", "cv_gap", "cv_1nn", "fisher_ratio")},
                })
        if not quiet:
            print(f"  {fam:22s} done ({len(rows)} rows, {time.time() - t_all:.1f}s)", flush=True)

        # baselines: deterministic given the split, so one row each
        for bname in config.get("baselines", []):
            b = BASELINES[bname]()
            b.fit(Xtr, ytr)
            rows.append({
                "family": fam, "mechanism": f"baseline_{bname}", "seed": base,
                "n_train": len(ytr), "n_test": len(yte),
                "train_accuracy": b.score(Xtr, ytr),
                "test_accuracy": b.score(Xte, yte),
                "n_states": 0,
                "n_params": int(getattr(b, "n_trainable_parameters", 0)),
                "fit_seconds": 0.0, "final_loss": float("nan"),
                **{k: geo[k] for k in
                   ("cv_linear", "cv_nonlinear", "cv_gap", "cv_1nn", "fisher_ratio")},
            })

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in FIELDS})

    env = {
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "rows": len(rows),
        "elapsed_seconds": round(time.time() - t_all, 2),
        "config": config,
    }
    env_path = os.path.splitext(out_path)[0] + "_env.json"
    with open(env_path, "w", encoding="utf-8") as f:
        json.dump(env, f, indent=2)

    if not quiet:
        print(f"\nwrote {len(rows)} rows -> {out_path}")
        print(f"environment   -> {env_path}")
        print(f"elapsed {env['elapsed_seconds']}s")
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default=os.path.join(ROOT, "experiments/configs/default.json"))
    ap.add_argument("--out", default=os.path.join(ROOT, "results/raw/fits.csv"))
    ap.add_argument("--force", action="store_true", help="replace an existing output file")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    with open(args.config, encoding="utf-8") as f:
        config = json.load(f)
    run(config, args.out, force=args.force, quiet=args.quiet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
