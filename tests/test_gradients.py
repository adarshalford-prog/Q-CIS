"""Requirement 6: analytic gradients must match finite differences."""

import numpy as np
import pytest

from qcis import QCISClassifier

MECHANISMS = ["coords_only", "incoherent", "fixed_phase", "trained_phase"]


def _prepared(mech, seed=1):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(24, 3))
    y = (rng.random(24) > 0.5).astype(int)
    m = QCISClassifier(mechanism=mech, n_states_per_class=4, dim=3)
    m.mean_ = X.mean(0)
    m.scale_ = X.std(0)
    m.scale_[m.scale_ < 1e-12] = 1.0
    Xs = (X - m.mean_) / m.scale_
    m._init_params(Xs, y, rng)
    return m, Xs, np.searchsorted(m.classes_, y), rng


@pytest.mark.parametrize("mech", MECHANISMS)
@pytest.mark.parametrize("param", ["W", "states", "log_sigma"])
def test_gradient_matches_finite_difference(mech, param):
    m, Xs, ye, rng = _prepared(mech)
    _, grads = m._loss_and_grads(Xs, ye)
    h = 1e-6

    def loss():
        return m._loss_and_grads(Xs, ye)[0]

    P = getattr(m, f"{param}_")
    if np.ndim(P) == 0:
        setattr(m, f"{param}_", float(P) + h)
        lp = loss()
        setattr(m, f"{param}_", float(P) - h)
        lm = loss()
        setattr(m, f"{param}_", float(P))
        num = (lp - lm) / (2 * h)
        ana = float(np.asarray(grads[param]))
        assert abs(num - ana) <= 1e-5 * max(1.0, abs(num), abs(ana)), (num, ana)
        return

    P = np.asarray(P)
    for _ in range(3):
        idx = tuple(int(rng.integers(0, s)) for s in P.shape)
        orig = P[idx]
        P[idx] = orig + h
        lp = loss()
        P[idx] = orig - h
        lm = loss()
        P[idx] = orig
        num = (lp - lm) / (2 * h)
        ana = float(np.asarray(grads[param])[idx])
        assert abs(num - ana) <= 1e-4 * max(1.0, abs(num), abs(ana)), (param, idx, num, ana)


@pytest.mark.parametrize("mech", ["fixed_phase", "trained_phase"])
def test_phase_gradient_matches_finite_difference(mech):
    m, Xs, ye, rng = _prepared(mech)
    _, grads = m._loss_and_grads(Xs, ye)
    h = 1e-6
    P = m.phi_
    for _ in range(4):
        i = int(rng.integers(0, len(P)))
        orig = P[i]
        P[i] = orig + h
        lp = m._loss_and_grads(Xs, ye)[0]
        P[i] = orig - h
        lm = m._loss_and_grads(Xs, ye)[0]
        P[i] = orig
        num = (lp - lm) / (2 * h)
        ana = float(np.asarray(grads["phi"])[i])
        assert abs(num - ana) <= 1e-4 * max(1.0, abs(num), abs(ana)), (i, num, ana)


@pytest.mark.parametrize("mech", ["coords_only", "incoherent"])
def test_phase_gradient_is_zero_when_phases_are_structurally_absent(mech):
    m, Xs, ye, _ = _prepared(mech)
    _, grads = m._loss_and_grads(Xs, ye)
    assert np.allclose(np.asarray(grads["phi"]), 0.0)


def test_cross_term_is_required():
    """Guard against the specific bug this release fixed.

    dL/dD_i must include the shift of the shared normaliser S = sum_j K_j, which
    makes every r_j depend on every D_i. Dropping those cross terms gives a
    state-dependent error that a spot check on one state can easily miss.
    """
    m, Xs, ye, _ = _prepared("coords_only")
    _, grads = m._loss_and_grads(Xs, ye)
    h = 1e-6
    P = m.states_
    # check several states, so a single-state coincidence cannot pass
    for i in range(P.shape[0]):
        idx = (i, 0)
        orig = P[idx]
        P[idx] = orig + h
        lp = m._loss_and_grads(Xs, ye)[0]
        P[idx] = orig - h
        lm = m._loss_and_grads(Xs, ye)[0]
        P[idx] = orig
        num = (lp - lm) / (2 * h)
        ana = float(np.asarray(grads["states"])[idx])
        assert abs(num - ana) <= 1e-4 * max(1.0, abs(num), abs(ana)), (i, num, ana)


def test_training_reduces_loss():
    m, Xs, ye, _ = _prepared("trained_phase")
    m2 = QCISClassifier("trained_phase", n_states_per_class=4, dim=3)
    X = Xs * m.scale_ + m.mean_
    y = m.classes_[ye]
    m2.fit(X, y, epochs=60, seed=0)
    assert m2.history_[-1] < m2.history_[0]
