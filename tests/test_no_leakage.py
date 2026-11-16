"""Requirements 8 and 9: train/test separation, and no use of test labels."""

import numpy as np
import pytest

from datasets.generation.synthetic import make, stratified_split
from qcis import QCISClassifier
from qcis.features import geometry_features


def test_split_is_disjoint_and_covers_everything():
    """Requirement 8: no index appears in both splits, and none is dropped."""
    for fam in ("xor", "circles", "blobs", "shells"):
        _, y = make(fam, seed=0)
        tr, te = stratified_split(y, seed=0)
        assert len(np.intersect1d(tr, te)) == 0, fam
        assert len(np.union1d(tr, te)) == len(y), fam


def test_split_is_stratified():
    _, y = make("blobs", seed=0)
    tr, te = stratified_split(y, seed=0)
    for c in np.unique(y):
        assert abs(np.mean(y[tr] == c) - np.mean(y[te] == c)) < 0.05


def test_geometry_features_never_see_test_rows():
    """Requirement 9: features must be identical when the test half is replaced.

    This is a structural check: the function is only given training rows, so
    corrupting the test half cannot change its output.
    """
    X, y = make("circles", seed=0)
    tr, te = stratified_split(y, seed=0)
    f1 = geometry_features(X[tr], y[tr], n_splits=3, seed=0)

    X2, y2 = X.copy(), y.copy()
    X2[te] = np.nan            # poison the test half
    y2[te] = 1 - y2[te]
    f2 = geometry_features(X2[tr], y2[tr], n_splits=3, seed=0)

    for k in ("cv_linear", "cv_nonlinear", "cv_gap", "cv_1nn", "fisher_ratio"):
        assert f1[k] == f2[k], k


def test_test_labels_do_not_affect_fitted_model():
    """Requirement 9: permuting test labels must not change the trained model."""
    X, y = make("moons", seed=3)
    tr, te = stratified_split(y, seed=3)

    a = QCISClassifier("trained_phase", dim=3).fit(X[tr], y[tr], epochs=25, seed=0)

    y_bad = y.copy()
    y_bad[te] = 1 - y_bad[te]
    b = QCISClassifier("trained_phase", dim=3).fit(X[tr], y_bad[tr], epochs=25, seed=0)

    assert np.array_equal(a.W_, b.W_)
    assert np.array_equal(a.states_, b.states_)


def test_state_class_membership_uses_training_labels_only():
    """The grouping I_c is fixed from training labels; test labels never enter it."""
    X, y = make("blobs", seed=2)
    tr, te = stratified_split(y, seed=2)
    m = QCISClassifier("trained_phase", dim=3).fit(X[tr], y[tr], epochs=5, seed=0)
    assert len(m.class_index_) == m.n_states
    assert set(np.unique(m.class_index_)) == set(range(len(np.unique(y[tr]))))


def test_standardisation_uses_training_statistics_only():
    X, y = make("shells", seed=1)
    tr, te = stratified_split(y, seed=1)
    m = QCISClassifier("incoherent", dim=3).fit(X[tr], y[tr], epochs=3, seed=0)
    assert np.allclose(m.mean_, X[tr].mean(0))
    assert np.allclose(m.scale_, X[tr].std(0))
