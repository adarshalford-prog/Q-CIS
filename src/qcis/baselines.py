"""Simple classical baselines.

These are reference points written for this release, deliberately kept small and
transparent. They are **not** the baseline implementations used in the historical
Phase 1-7 runs, which were never published, so they cannot be used to reproduce
statements such as "Q-CIS was behind RBF by 3.33 points". They exist so that a
reader can see whether a coordinate-and-phase model does anything on a given
family that a trivial geometric classifier does not.

Included:
    NearestCentroid      - class means, Euclidean nearest mean.
    RBFRidgeClassifier   - Gaussian-kernel ridge regression on one-hot targets,
                           with the regularisation strength chosen by 5-fold CV.
"""

from __future__ import annotations

import numpy as np

from .features import _one_hot, median_gamma, probe_cv_accuracy, stratified_folds


class NearestCentroid:
    """Nearest class mean under Euclidean distance."""

    name = "nearest_centroid"

    def fit(self, X, y):
        X = np.asarray(X, float)
        y = np.asarray(y)
        self.classes_ = np.unique(y)
        self.means_ = np.vstack([X[y == c].mean(0) for c in self.classes_])
        return self

    def predict(self, X):
        X = np.asarray(X, float)
        d = ((X[:, None, :] - self.means_[None, :, :]) ** 2).sum(-1)
        return self.classes_[np.argmin(d, axis=1)]

    def score(self, X, y):
        return float(np.mean(self.predict(X) == np.asarray(y)))


class RBFRidgeClassifier:
    """Gaussian-kernel ridge classifier on one-hot targets."""

    name = "rbf_ridge"

    def __init__(self, lambdas=(0.01, 0.1, 1.0, 10.0), n_splits=5, seed=0):
        self.lambdas = lambdas
        self.n_splits = n_splits
        self.seed = seed

    def fit(self, X, y):
        X = np.asarray(X, float)
        y = np.asarray(y)
        self.classes_ = np.unique(y)
        self.gamma_ = median_gamma(X)
        best = (-np.inf, self.lambdas[0])
        for lam in self.lambdas:
            Y = _one_hot(y, self.classes_)
            preds = np.empty(len(y), dtype=int)
            for tr, va in stratified_folds(y, self.n_splits, self.seed):
                K = np.exp(-self.gamma_ * ((X[tr][:, None, :] - X[tr][None, :, :]) ** 2).sum(-1))
                a = np.linalg.solve(K + lam * np.eye(len(K)), Y[tr])
                Kv = np.exp(-self.gamma_ * ((X[va][:, None, :] - X[tr][None, :, :]) ** 2).sum(-1))
                preds[va] = np.argmax(Kv @ a, axis=1)
            acc = float(np.mean(self.classes_[preds] == y))
            if acc > best[0]:
                best = (acc, lam)
        self.lambda_ = best[1]
        self.cv_accuracy_ = best[0]
        K = np.exp(-self.gamma_ * ((X[:, None, :] - X[None, :, :]) ** 2).sum(-1))
        self.alpha_ = np.linalg.solve(K + self.lambda_ * np.eye(len(K)), _one_hot(y, self.classes_))
        self._X = X
        return self

    def predict(self, X):
        X = np.asarray(X, float)
        Kv = np.exp(-self.gamma_ * ((X[:, None, :] - self._X[None, :, :]) ** 2).sum(-1))
        return self.classes_[np.argmax(Kv @ self.alpha_, axis=1)]

    def score(self, X, y):
        return float(np.mean(self.predict(X) == np.asarray(y)))

    @property
    def n_trainable_parameters(self):
        return int(self.alpha_.size)


BASELINES = {"nearest_centroid": NearestCentroid, "rbf_ridge": RBFRidgeClassifier}
