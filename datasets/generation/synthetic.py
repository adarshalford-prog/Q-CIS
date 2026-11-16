"""Synthetic dataset generators.

Every generator is deterministic given its seed and parameters, and is documented
here in full so an outside researcher can regenerate exactly the same data. No
external dataset is used anywhere in this repository, so there is nothing to
download and no third-party data licence to observe.

These generators are written for this reference release. They produce dataset
*families* of the same shape as those described in ``docs/phase_history.md``
(XOR, concentric circles, overlapping clusters, spirals, moons, rings, shells),
but they are not the original generators used for the Phase 1-7 runs, which were
never published. Numbers produced here therefore cannot be compared with the
historical figures.
"""

from __future__ import annotations

import numpy as np

# --------------------------------------------------------------------- helpers


def _as_d(n, d, base):
    """Pad or truncate a 2-D design to ``d`` columns with small deterministic noise."""
    base = np.asarray(base, dtype=float)
    if base.shape[1] == d:
        return base
    if base.shape[1] > d:
        return base[:, :d]
    rng = np.random.default_rng(1000 * d + base.shape[0])
    pad = rng.normal(0.0, 0.05, size=(base.shape[0], d - base.shape[1]))
    return np.hstack([base, pad])


def _split_counts(n, k):
    base = n // k
    counts = np.full(k, base)
    counts[: n - base * k] += 1
    return counts


# ------------------------------------------------------------------ generators


def xor(n=400, d=2, noise=0.15, seed=0):
    """Four clusters at the corners of a square; the label is the XOR of the signs.

    Linearly inseparable: no single hyperplane solves it. Tests nonlinear separability.
    """
    rng = np.random.default_rng(seed)
    per = _split_counts(n, 4)
    centres = np.array([[1, 1], [1, -1], [-1, 1], [-1, -1]], dtype=float)
    labels = np.array([0, 1, 1, 0])
    X, y = [], []
    for c, lab, k in zip(centres, labels, per):
        X.append(c + rng.normal(0.0, noise, size=(k, 2)))
        y.append(np.full(k, lab))
    X = np.vstack(X)
    y = np.concatenate(y)
    idx = rng.permutation(len(y))
    return _as_d(len(y), d, X[idx]), y[idx]


def circles(n=400, d=2, noise=0.10, seed=0):
    """Two concentric circles. Tests curved decision boundaries."""
    rng = np.random.default_rng(seed)
    per = _split_counts(n, 2)
    X, y = [], []
    for r, lab, k in ((1.0, 0, per[0]), (2.0, 1, per[1])):
        t = rng.uniform(0, 2 * np.pi, size=k)
        pts = np.c_[r * np.cos(t), r * np.sin(t)]
        X.append(pts + rng.normal(0.0, noise, size=(k, 2)))
        y.append(np.full(k, lab))
    X = np.vstack(X)
    y = np.concatenate(y)
    idx = rng.permutation(len(y))
    return _as_d(len(y), d, X[idx]), y[idx]


def overlapping_clusters(n=400, d=2, noise=0.85, seed=0):
    """Two heavily overlapping Gaussian blobs. Tests ambiguity and irreducible error."""
    rng = np.random.default_rng(seed)
    per = _split_counts(n, 2)
    X = np.vstack([
        rng.normal([-0.5, 0.0], noise, size=(per[0], 2)),
        rng.normal([+0.5, 0.0], noise, size=(per[1], 2)),
    ])
    y = np.concatenate([np.zeros(per[0], int), np.ones(per[1], int)])
    idx = rng.permutation(len(y))
    return _as_d(len(y), d, X[idx]), y[idx]


def spirals(n=400, d=2, noise=0.08, turns=1.5, seed=0):
    """Two interleaved Archimedean spirals. The task where phase effects were reported
    to matter most in the historical record."""
    rng = np.random.default_rng(seed)
    per = _split_counts(n, 2)
    X, y = [], []
    for c, k in ((0, per[0]), (1, per[1])):
        t = np.sqrt(rng.uniform(0, 1, size=k)) * turns * 2 * np.pi
        r = t / (turns * 2 * np.pi)
        pts = np.c_[r * np.cos(t) + c * 0.6, r * np.sin(t) + c * 0.6]
        X.append(pts + rng.normal(0.0, noise, size=(k, 2)))
        y.append(np.full(k, c))
    X = np.vstack(X)
    y = np.concatenate(y)
    idx = rng.permutation(len(y))
    return _as_d(len(y), d, X[idx]), y[idx]


def moons(n=400, d=2, noise=0.10, seed=0):
    """Two interleaving half circles ('two moons')."""
    rng = np.random.default_rng(seed)
    per = _split_counts(n, 2)
    t0 = rng.uniform(0, np.pi, size=per[0])
    t1 = rng.uniform(0, np.pi, size=per[1])
    X0 = np.c_[np.cos(t0), np.sin(t0)]
    X1 = np.c_[1 - np.cos(t1), 1 - np.sin(t1) - 0.5]
    X = np.vstack([X0, X1]) + rng.normal(0.0, noise, size=(n, 2))
    y = np.concatenate([np.zeros(per[0], int), np.ones(per[1], int)])
    idx = rng.permutation(len(y))
    return _as_d(len(y), d, X[idx]), y[idx]


def rings(n=400, d=2, noise=0.05, seed=0, n_rings=4):
    """Alternating concentric rings. A family where the historical record reports Q-CIS
    losing badly to RBF (see RESULTS_SUMMARY.md)."""
    rng = np.random.default_rng(seed)
    per = _split_counts(n, n_rings)
    X, y = [], []
    for i, k in enumerate(per):
        r = 0.6 + 0.45 * i
        t = rng.uniform(0, 2 * np.pi, size=k)
        X.append(np.c_[r * np.cos(t), r * np.sin(t)] + rng.normal(0.0, noise, size=(k, 2)))
        y.append(np.full(k, i % 2))
    X = np.vstack(X)
    y = np.concatenate(y)
    idx = rng.permutation(len(y))
    return _as_d(len(y), d, X[idx]), y[idx]


def shells(n=400, d=20, noise=0.05, seed=0):
    """Two concentric high-dimensional shells. The high-dimensional family where the
    historical record reports phases being actively harmful (coherent 51.0 vs
    incoherent 58.2, with RBF at 96.0)."""
    rng = np.random.default_rng(seed)
    per = _split_counts(n, 2)
    X, y = [], []
    for r, lab, k in ((1.0, 0, per[0]), (1.35, 1, per[1])):
        v = rng.normal(size=(k, d))
        v /= np.linalg.norm(v, axis=1, keepdims=True)
        X.append(v * r + rng.normal(0.0, noise, size=(k, d)))
        y.append(np.full(k, lab))
    X = np.vstack(X)
    y = np.concatenate(y)
    idx = rng.permutation(len(y))
    return X[idx], y[idx]


def blobs(n=400, d=4, noise=0.6, seed=0):
    """A well-separated three-class control task."""
    rng = np.random.default_rng(seed)
    per = _split_counts(n, 3)
    centres = rng.normal(0.0, 2.0, size=(3, d))
    X = np.vstack([rng.normal(centres[i], noise, size=(per[i], d)) for i in range(3)])
    y = np.concatenate([np.full(per[i], i) for i in range(3)])
    idx = rng.permutation(len(y))
    return X[idx], y[idx]


GENERATORS = {
    "xor": xor,
    "circles": circles,
    "overlapping_clusters": overlapping_clusters,
    "spirals": spirals,
    "moons": moons,
    "rings": rings,
    "shells": shells,
    "blobs": blobs,
}

# Documented family registry: name -> (generator kwargs). This is the exact
# configuration used by scripts/run_reproduction.py.
FAMILIES = {
    "xor": {"n": 400, "d": 2, "noise": 0.15},
    "circles": {"n": 400, "d": 2, "noise": 0.10},
    "overlapping_clusters": {"n": 400, "d": 2, "noise": 0.85},
    "spirals": {"n": 400, "d": 2, "noise": 0.08},
    "moons": {"n": 400, "d": 2, "noise": 0.10},
    "rings": {"n": 400, "d": 2, "noise": 0.05},
    "shells": {"n": 400, "d": 20, "noise": 0.05},
    "blobs": {"n": 400, "d": 4, "noise": 0.60},
}


def make(name, seed=0, **overrides):
    """Generate one dataset family by name."""
    if name not in GENERATORS:
        raise KeyError(f"unknown family {name!r}; available: {sorted(GENERATORS)}")
    kw = dict(FAMILIES.get(name, {}))
    kw.update(overrides)
    return GENERATORS[name](seed=seed, **kw)


def stratified_split(y, test_frac=0.3, seed=0):
    """Deterministic stratified train/test split.

    The split is drawn from ``seed`` alone, so the same seed always yields the same
    partition. Test indices are never touched by any fitting or feature construction
    routine; see ``tests/test_no_leakage.py``.
    """
    rng = np.random.default_rng(seed)
    y = np.asarray(y)
    train_idx, test_idx = [], []
    for c in np.unique(y):
        idx = np.flatnonzero(y == c)
        idx = rng.permutation(idx)
        n_test = int(round(len(idx) * test_frac))
        test_idx.append(idx[:n_test])
        train_idx.append(idx[n_test:])
    tr = np.sort(np.concatenate(train_idx))
    te = np.sort(np.concatenate(test_idx))
    return tr, te
