#!/usr/bin/env python3
"""Family-level statistical analysis of a benchmark run.

Implements the corrected inference described in ``docs/statistical_audit_summary.md``:

* the **dataset family** is the independent unit, not the individual seed-level fit;
* seeds within a family are averaged before any comparison;
* paired comparisons are bootstrapped across families;
* multiplicity is controlled with Holm across the reported contrasts.

Writes a machine-readable JSON and a human-readable Markdown summary.

Usage
-----
    python analysis/audit.py --fits results/raw/fits.csv --outdir results/summaries
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from qcis import selectors, stats  # noqa: E402

CONTRASTS = [
    ("trained_phase", "incoherent"),
    ("trained_phase", "coords_only"),
    ("trained_phase", "fixed_phase"),
    ("incoherent", "coords_only"),
    ("trained_phase", "baseline_rbf_ridge"),
    ("trained_phase", "baseline_nearest_centroid"),
]


def spearman(a, b):
    """Spearman rank correlation, with a plain permutation-free asymptotic note only.

    Returns (rho, n). No p-value is computed here; the small number of families makes
    an asymptotic p-value misleading, which is exactly the error the historical audit
    corrected.
    """
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    if len(a) < 3:
        return float("nan"), len(a)
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean()
    rb -= rb.mean()
    denom = np.sqrt((ra ** 2).sum() * (rb ** 2).sum())
    return float((ra * rb).sum() / denom) if denom > 0 else float("nan"), len(a)


def load(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def analyse(rows, n_boot=10000, seed=0):
    for r in rows:
        r["accuracy"] = float(r["test_accuracy"])
        r["cv_gap"] = float(r["cv_gap"])

    families = sorted({r["family"] for r in rows})
    mechanisms = sorted({r["mechanism"] for r in rows})

    # family-level means (seeds averaged first: the family is the unit)
    means = stats.family_means(rows, "family", "accuracy")

    # per-family geometry feature (constant within a family)
    gap_by_family = {}
    for r in rows:
        gap_by_family.setdefault(r["family"], r["cv_gap"])

    out = {
        "n_fits": len(rows),
        "n_families": len(families),
        "families": families,
        "mechanisms": mechanisms,
        "family_level_means": {
            f: {m: round(means[(f, m)], 4) for m in mechanisms if (f, m) in means}
            for f in families
        },
        "overall_means": {
            m: round(float(np.mean([means[(f, m)] for f in families if (f, m) in means])), 4)
            for m in mechanisms
        },
        "unit": "dataset family (seeds averaged within family)",
        "n_independent_units": len(families),
    }

    # paired family-level contrasts
    contrasts = []
    for a, b in CONTRASTS:
        if not all((f, a) in means and (f, b) in means for f in families):
            continue
        c = stats.compare(means, a, b, families, n_boot=n_boot, seed=seed)
        c["mean_pp"] = round(100.0 * c["mean"], 3)
        c["ci_low_pp"] = round(100.0 * c["ci_low"], 3)
        c["ci_high_pp"] = round(100.0 * c["ci_high"], 3)
        contrasts.append(c)
    if contrasts:
        adj = stats.holm_adjust([c["p_value"] for c in contrasts])
        for c, p in zip(contrasts, adj):
            c["p_value"] = round(float(c["p_value"]), 5)
            c["p_holm"] = round(float(p), 5)
            c["distinguishable_from_zero"] = bool(p < 0.05)
    out["contrasts"] = contrasts

    # does the geometry gap track the measured phase benefit?
    benefit = []
    gaps = []
    for f in families:
        if (f, "trained_phase") in means and (f, "incoherent") in means:
            benefit.append(means[(f, "trained_phase")] - means[(f, "incoherent")])
            gaps.append(gap_by_family[f])
    rho, n = spearman(gaps, benefit)
    out["geometry_gap_vs_phase_benefit"] = {
        "spearman_rho": round(rho, 4) if rho == rho else None,
        "n_families": n,
        "note": (
            "Descriptive only. With this many families an asymptotic p-value would be "
            "misleading; the historical audit's central correction was exactly that the "
            "family, not the fit, is the unit of inference."
        ),
        "per_family": {
            f: {"cv_gap": round(gap_by_family[f], 4),
                "phase_benefit_pp": round(100.0 * (means[(f, "trained_phase")] - means[(f, "incoherent")]), 3)}
            for f in families if (f, "trained_phase") in means and (f, "incoherent") in means
        },
    }

    # frozen selector behaviour on this bank
    sel = {}
    for name, fn in selectors.SELECTORS.items():
        correct = 0
        comparable = 0
        chosen = {}
        for f in families:
            if not ((f, "trained_phase") in means and (f, "incoherent") in means):
                continue
            pick = fn(np.array([gap_by_family[f]]))[0]
            chosen[f] = pick
            best = max(means[(f, "trained_phase")], means[(f, "incoherent")])
            if abs(means[(f, "trained_phase")] - means[(f, "incoherent")]) < 1e-9:
                continue  # tie: not scored
            comparable += 1
            if abs(means[(f, pick)] - best) < 1e-9:
                correct += 1
        sel[name] = {
            "correct": correct,
            "comparable_families": comparable,
            "accuracy": round(correct / comparable, 4) if comparable else None,
            "choices": chosen,
        }
    out["frozen_selectors"] = sel
    out["frozen_selectors_note"] = (
        "D1 and D2 are the two frozen formulas whose constants are published. D3 is not "
        "implemented because its threshold and corrected polarity are not recorded in the "
        "published material. These numbers exercise the selector mechanism on newly "
        "generated data; they do not reproduce the historical selector results."
    )
    return out


def to_markdown(res, fits_path):
    L = []
    L.append("# Q-CIS benchmark summary — reference implementation 0.2.0\n")
    L.append(f"Generated from `{os.path.basename(fits_path)}`.\n")
    L.append("> **What this is.** Output of the reference implementation in `src/qcis`, run on "
             "freshly generated synthetic families. It is **not** a reproduction of the "
             "historical Phase 1–7 figures, whose code, data and configurations were never "
             "published. See `REPOSITORY_AUDIT.md`.\n")
    L.append(f"**Independent unit:** {res['unit']}  \n"
             f"**Fits:** {res['n_fits']}  \n"
             f"**Families:** {res['n_families']}\n")

    L.append("\n## Family-level means (test accuracy)\n")
    mechs = res["mechanisms"]
    L.append("| Family | " + " | ".join(mechs) + " |")
    L.append("|---" * (len(mechs) + 1) + "|")
    for f in res["families"]:
        row = res["family_level_means"][f]
        L.append(f"| {f} | " + " | ".join(f"{row.get(m, float('nan')):.3f}" for m in mechs) + " |")
    L.append("| **mean** | " + " | ".join(f"**{res['overall_means'].get(m, float('nan')):.3f}**" for m in mechs) + " |")

    L.append("\n## Paired family-level contrasts\n")
    L.append("| Contrast | Mean diff (pp) | 95% CI (pp) | p | p (Holm) | Distinguishable from zero |")
    L.append("|---|---|---|---|---|---|")
    for c in res["contrasts"]:
        L.append(
            f"| {c['contrast']} | {c['mean_pp']:+.2f} | [{c['ci_low_pp']:+.2f}, {c['ci_high_pp']:+.2f}] "
            f"| {c['p_value']:.4f} | {c['p_holm']:.4f} | {'yes' if c['distinguishable_from_zero'] else 'no'} |"
        )
    L.append("\nA contrast that is not distinguishable from zero is **inconclusive**. It is not "
             "evidence of equivalence.\n")

    g = res["geometry_gap_vs_phase_benefit"]
    L.append(f"\n## Geometry gap vs measured phase benefit\n")
    L.append(f"Spearman rho = {g['spearman_rho']} over {g['n_families']} families (descriptive only).\n")
    L.append("| Family | cv_gap | phase benefit (pp) |")
    L.append("|---|---|---|")
    for f, v in g["per_family"].items():
        L.append(f"| {f} | {v['cv_gap']:+.4f} | {v['phase_benefit_pp']:+.2f} |")

    L.append("\n## Frozen selectors\n")
    L.append("| Selector | Correct | Comparable families | Accuracy |")
    L.append("|---|---|---|---|")
    for k, v in res["frozen_selectors"].items():
        L.append(f"| {k} | {v['correct']} | {v['comparable_families']} | {v['accuracy']} |")
    L.append(f"\n{res['frozen_selectors_note']}\n")
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fits", default=os.path.join(ROOT, "results/raw/fits.csv"))
    ap.add_argument("--outdir", default=os.path.join(ROOT, "results/summaries"))
    ap.add_argument("--n-boot", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=20261116)
    args = ap.parse_args(argv)

    rows = load(args.fits)
    if not rows:
        raise SystemExit(f"no rows in {args.fits}")
    res = analyse(rows, n_boot=args.n_boot, seed=args.seed)

    os.makedirs(args.outdir, exist_ok=True)
    with open(os.path.join(args.outdir, "audit.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    md = to_markdown(res, args.fits)
    with open(os.path.join(args.outdir, "summary.md"), "w", encoding="utf-8") as f:
        f.write(md)

    with open(os.path.join(args.outdir, "summary.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["family"] + res["mechanisms"])
        for fam in res["families"]:
            w.writerow([fam] + [f"{res['family_level_means'][fam].get(m, ''):.6f}"
                                if m in res["family_level_means"][fam] else ""
                                for m in res["mechanisms"]])

    print(f"families: {res['n_families']}   fits: {res['n_fits']}")
    for m, v in res["overall_means"].items():
        print(f"  {m:32s} {v:.4f}")
    print("\ncontrasts (family level, Holm-adjusted):")
    for c in res["contrasts"]:
        flag = "significant" if c["distinguishable_from_zero"] else "not distinguishable"
        print(f"  {c['contrast']:44s} {c['mean_pp']:+.2f}pp "
              f"[{c['ci_low_pp']:+.2f}, {c['ci_high_pp']:+.2f}]  p_holm={c['p_holm']:.4f}  {flag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
