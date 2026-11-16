"""Statistics used to compare mechanisms across dataset families.

The inferential unit here is the **dataset family**, not the individual fit. A family
contributes one number per mechanism (the mean over seeds), and paired comparisons
are made across families. This is the correction recorded in the Phase 7 statistical
audit: treating each seed-level fit as independent inflates the apparent evidence,
because seeds within a family are not independent draws of a new task.

Every function is deterministic given a seed.
"""

from __future__ import annotations

import numpy as np


# ------------------------------------------------------------- paired bootstrap


def paired_bootstrap_ci(
    diff: np.ndarray, n_boot: int = 10000, alpha: float = 0.05, seed: int = 0
) -> dict:
    """Percentile bootstrap confidence interval for the mean of paired differences.

    Parameters
    ----------
    diff : array of paired differences, one entry per independent unit (family).

    Returns
    -------
    dict with ``mean``, ``ci_low``, ``ci_high``, ``n``, ``n_boot``, ``alpha``.
    """
    diff = np.asarray(diff, dtype=float)
    diff = diff[np.isfinite(diff)]
    n = len(diff)
    if n == 0:
        return {"mean": float("nan"), "ci_low": float("nan"), "ci_high": float("nan"),
                "n": 0, "n_boot": n_boot, "alpha": alpha}
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(n_boot, n))
    boot = diff[idx].mean(axis=1)
    lo, hi = np.quantile(boot, [alpha / 2, 1 - alpha / 2])
    return {
        "mean": float(diff.mean()),
        "ci_low": float(lo),
        "ci_high": float(hi),
        "n": int(n),
        "n_boot": int(n_boot),
        "alpha": float(alpha),
    }


def bootstrap_p_value(diff: np.ndarray, n_boot: int = 10000, seed: int = 0) -> float:
    """Two-sided bootstrap p-value for the mean of paired differences being zero.

    Computed by inverting the percentile interval: the smallest alpha at which the
    interval excludes zero, equivalently twice the smaller tail mass.
    """
    diff = np.asarray(diff, dtype=float)
    diff = diff[np.isfinite(diff)]
    n = len(diff)
    if n == 0:
        return float("nan")
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(n_boot, n))
    boot = diff[idx].mean(axis=1)
    p_lo = float(np.mean(boot <= 0))
    p_hi = float(np.mean(boot >= 0))
    return float(min(1.0, 2.0 * min(p_lo, p_hi)))


# --------------------------------------------------- multiple-comparison control


def holm_adjust(pvals) -> np.ndarray:
    """Holm-Bonferroni step-down adjusted p-values (Holm 1979)."""
    p = np.asarray(pvals, dtype=float)
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m, dtype=float)
    running = 0.0
    for rank, i in enumerate(order):
        val = (m - rank) * p[i]
        running = max(running, val)
        adj[i] = min(1.0, running)
    return adj


def bh_adjust(pvals) -> np.ndarray:
    """Benjamini-Hochberg false-discovery-rate adjusted p-values (1995)."""
    p = np.asarray(pvals, dtype=float)
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m, dtype=float)
    running = 1.0
    for rank in range(m - 1, -1, -1):
        i = order[rank]
        val = p[i] * m / (rank + 1)
        running = min(running, val)
        adj[i] = min(1.0, running)
    return adj


# --------------------------------------------------------------------- McNemar


def mcnemar(b_correct: np.ndarray, c_correct: np.ndarray) -> dict:
    """McNemar's test on two paired boolean correctness vectors.

    Returns the discordant counts and the exact binomial two-sided p-value.
    """
    b = np.asarray(b_correct, dtype=bool)
    c = np.asarray(c_correct, dtype=bool)
    n01 = int(np.sum(~b & c))   # b wrong, c right
    n10 = int(np.sum(b & ~c))   # b right, c wrong
    n = n01 + n10
    if n == 0:
        return {"n01": 0, "n10": 0, "p_value": 1.0}
    # exact two-sided binomial test with p = 0.5
    from math import comb
    k = min(n01, n10)
    tail = sum(comb(n, i) for i in range(0, k + 1)) / (2 ** n)
    return {"n01": n01, "n10": n10, "p_value": float(min(1.0, 2 * tail))}


# ------------------------------------------------------- family-level aggregation


def family_means(rows, family_key="family", value_key="accuracy"):
    """Collapse seed-level rows to one value per (family, mechanism).

    ``rows`` is a sequence of dicts. Returns a dict ``{(family, mechanism): mean}``.
    """
    acc = {}
    for r in rows:
        key = (r[family_key], r["mechanism"])
        acc.setdefault(key, []).append(float(r[value_key]))
    return {k: float(np.mean(v)) for k, v in acc.items()}


def paired_family_differences(means, fam_a: str, fam_b: str, families):
    """Paired per-family differences ``mean(a) - mean(b)`` over the given families."""
    out = []
    for f in families:
        ka, kb = (f, fam_a), (f, fam_b)
        if ka in means and kb in means:
            out.append(means[ka] - means[kb])
    return np.asarray(out, dtype=float)


def compare(means, fam_a, fam_b, families, n_boot=10000, seed=0) -> dict:
    """Full paired family-level comparison between two mechanisms."""
    diff = paired_family_differences(means, fam_a, fam_b, families)
    ci = paired_bootstrap_ci(diff, n_boot=n_boot, seed=seed)
    ci["p_value"] = bootstrap_p_value(diff, n_boot=n_boot, seed=seed)
    ci["contrast"] = f"{fam_a} - {fam_b}"
    return ci
