"""Requirement 7: fixed seeds give bit-identical results."""

import numpy as np

from datasets.generation.synthetic import make, stratified_split
from qcis import QCISClassifier


def test_same_seed_same_parameters():
    X, y = make("spirals", seed=7)
    tr, te = stratified_split(y, seed=7)
    a = QCISClassifier("trained_phase", dim=3).fit(X[tr], y[tr], epochs=30, seed=3)
    b = QCISClassifier("trained_phase", dim=3).fit(X[tr], y[tr], epochs=30, seed=3)
    assert np.array_equal(a.W_, b.W_)
    assert np.array_equal(a.states_, b.states_)
    assert np.array_equal(a.phi_, b.phi_)
    assert np.array_equal(a.predict(X[te]), b.predict(X[te]))
    assert np.allclose(a.predict_proba(X[te]), b.predict_proba(X[te]), atol=0, rtol=0)


def test_different_seed_changes_initialisation():
    X, y = make("spirals", seed=7)
    a = QCISClassifier("trained_phase", dim=3).fit(X, y, epochs=5, seed=0)
    b = QCISClassifier("trained_phase", dim=3).fit(X, y, epochs=5, seed=1)
    assert not np.array_equal(a.W_, b.W_)


def test_generators_are_deterministic():
    for fam in ("xor", "circles", "rings", "shells"):
        X1, y1 = make(fam, seed=11)
        X2, y2 = make(fam, seed=11)
        assert np.array_equal(X1, X2), fam
        assert np.array_equal(y1, y2), fam


def test_splits_are_deterministic():
    _, y = make("blobs", seed=1)
    a = stratified_split(y, seed=5)
    b = stratified_split(y, seed=5)
    assert np.array_equal(a[0], b[0]) and np.array_equal(a[1], b[1])
