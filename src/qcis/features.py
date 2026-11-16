"""Geometry features computed with cross-validation.

The historical record describes a "nonlinear-minus-linear probe gap" that correlated
with the benefit of phase interference. The *exact* probe implementation used for the
Phase 5-7 runs was never published, so this module is **this release's own reproducible
definition** of those features, not a reconstruction of the original one. Numbers here
are therefore not comparable with the historical correlation figures.

Design rules enforced here and tested in ``tests/test_no_leakage.py``:

* every feature is computed from the training split only;
* no test label, and no test row, is passed to any function in this module;
* the probes use stratified k-fold cross-validation *within* the training split, so
  the reported accuracy is an out-of-fold estimate on training data.
"""

from __future__ import annotations

import numpy as np


# --------------------------------------------------------------------- encoding


def _one_hot(y, classes):
    Y = np.zeros((len(y), len(classes)))
    Y[np.arange(len(y)), np.searchsorted(classes, y)] = 1.0
    return Y


def stratified_folds(y, n_splits=5, seed=0):
    """Yield (train_idx, valid_idx) for stratified k-fold CV."""
    rng = np.random.default_rng(seed)
    y = np.asarray(y)
    folds = [[] for _ in range(n_splits)]
    for c in np.unique(y):
        idx = rng.permutation(np.flatnonzero(y == c))
        for j, chunk in enumerate(np.array_split(idx, n_splits)):
            folds[j].extend(chunk.tolist())
    all_idx = np.arange(len(y))
    for j in range(n_splits):
        valid = np.array(sorted(folds[j]), dtype=int)
        train = np.setdiff1d(all_idx, valid)
        yield train, valid


# ----------------------------------------------------------------------- probes


def _ridge_fit_predict(Xtr, Ytr, Xva, lam):
    Xtr = np.asarray(Xtr, float)
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd[sd < 1e-12] = 1.0
    A = (Xtr - mu) / sd
    B = (np.asarray(Xva, float) - mu) / sd
    d = A.shape[1]
    W = np.linalg.solve(A.T @ A + lam * np.eye(d), A.T @ Ytr)
    return B @ W


def _rbf_kernel(A, B, gamma):
    d = ((A[:, None, :] - B[None, :, :]) ** 2).sum(-1)
    return np.exp(-gamma * d)


def _kernel_ridge_fit_predict(Xtr, Ytr, Xva, lam, gamma):
    K = _rbf_kernel(Xtr, Xtr, gamma)
    alpha = np.linalg.solve(K + lam * np.eye(len(K)), Ytr)
    return _rbf_kernel(Xva, Xtr, gamma) @ alpha


def _cv_accuracy(X, y, classes, probe, lam, n_splits, seed, gamma=None):
    """Out-of-fold accuracy for one probe and one regularisation strength."""
    Y = _one_hot(y, classes)
    preds = np.empty(len(y), dtype=int)
    for tr, va in stratified_folds(y, n_splits=n_splits, seed=seed):
        if probe == "linear":
            scores = _ridge_fit_predict(X[tr], Y[tr], X[va], lam)
        else:
            scores = _kernel_ridge_fit_predict(X[tr], Y[tr], X[va], lam, gamma)
        preds[va] = np.argmax(scores, axis=1)
    return float(np.mean(classes[preds] == y))


def median_gamma(X):
    """Median heuristic bandwidth for the RBF probe (training data only)."""
    X = np.asarray(X, float)
    d = ((X[:, None, :] - X[None, :, :]) ** 2).sum(-1)
    med = np.median(d[d > 0]) if np.any(d > 0) else 1.0
    return float(1.0 / max(med, 1e-12))


def probe_cv_accuracy(
    X, y, probe="linear", lambdas=(0.01, 0.1, 1.0, 10.0), n_splits=5, seed=0
):
    """Best cross-validated accuracy over the documented regularisation grid.

    ``lambdas`` is the same grid described in the historical record
    ({0.01, 0.1, 1, 10}). Returns (accuracy, chosen_lambda).
    """
    classes = np.unique(y)
    gamma = median_gamma(X) if probe == "rbf" else None
    best = (-np.inf, None)
    for lam in lambdas:
        acc = _cv_accuracy(X, y, classes, probe, lam, n_splits, seed, gamma)
        if acc > best[0]:
            best = (acc, lam)
    return float(best[0]), float(best[1])


def cv_1nn_accuracy(X, y, n_splits=5, seed=0):
    """Out-of-fold 1-nearest-neighbour accuracy, as a reference point."""
    classes = np.unique(y)
    preds = np.empty(len(y), dtype=int)
    for tr, va in stratified_folds(y, n_splits=n_splits, seed=seed):
        d = ((X[va][:, None, :] - X[tr][None, :, :]) ** 2).sum(-1)
        preds[va] = np.searchsorted(classes, y[tr][np.argmin(d, axis=1)])
    return float(np.mean(classes[preds] == y))


def fisher_ratio(X, y):
    """Between-class over within-class scatter ratio (a linear separability proxy)."""
    X = np.asarray(X, float)
    y = np.asarray(y)
    classes = np.unique(y)
    overall = X.mean(0)
    between = 0.0
    within = 0.0
    for c in classes:
        Xc = X[y == c]
        if len(Xc) == 0:
            continue
        mc = Xc.mean(0)
        between += len(Xc) * float(((mc - overall) ** 2).sum())
        within += float(((Xc - mc) ** 2).sum())
    return float(between / max(within, 1e-12))


def geometry_features(X_train, y_train, n_splits=5, seed=0):
    """All geometry features for one dataset family, from training data only.

    Returns a dict with ``cv_linear``, ``cv_nonlinear``, ``cv_gap``, ``cv_1nn``
    and ``fisher_ratio``.
    """
    X_train = np.asarray(X_train, float)
    y_train = np.asarray(y_train)
    lin, lam_lin = probe_cv_accuracy(X_train, y_train, "linear", n_splits=n_splits, seed=seed)
    nl, lam_nl = probe_cv_accuracy(X_train, y_train, "rbf", n_splits=n_splits, seed=seed)
    return {
        "cv_linear": lin,
        "cv_nonlinear": nl,
        "cv_gap": float(nl - lin),
        "cv_1nn": cv_1nn_accuracy(X_train, y_train, n_splits=n_splits, seed=seed),
        "fisher_ratio": fisher_ratio(X_train, y_train),
        "lambda_linear": lam_lin,
        "lambda_nonlinear": lam_nl,
        "n_train": int(len(y_train)),
    }
