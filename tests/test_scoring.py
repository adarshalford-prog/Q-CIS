"""Mathematical properties of the score function (requirements 1-5)."""

import numpy as np
import pytest

from qcis.scoring import (
    class_scores,
    class_scores_complex,
    class_scores_real,
    gaussian_similarity,
    normalized_magnitudes,
    probabilities,
    squared_distances,
)

RNG = np.random.default_rng(12345)


def _problem(n=12, S=8, C=2):
    q = RNG.normal(size=(n, 3))
    states = RNG.normal(size=(S, 3))
    class_index = np.array([i % C for i in range(S)])
    phi = RNG.uniform(-np.pi, np.pi, size=S)
    D = squared_distances(q, states)
    K = gaussian_similarity(D, 0.9)
    r = normalized_magnitudes(K)
    return q, states, class_index, phi, D, K, r


def test_normalized_magnitudes_sum_to_one():
    """Requirement 1: sum_i r_i^2 == 1."""
    *_, r = _problem()
    assert np.allclose((r ** 2).sum(axis=1), 1.0, atol=1e-12)


def test_normalized_magnitudes_sum_to_one_extreme_scales():
    """Requirement 1, also at distance scales where K spans many orders of magnitude."""
    for scale in (1e-6, 1.0, 1e6):
        D = np.abs(RNG.normal(size=(5, 6))) * scale
        r = normalized_magnitudes(gaussian_similarity(D, 1.0))
        assert np.allclose((r ** 2).sum(axis=1), 1.0, atol=1e-12), scale


def test_complex_and_real_scores_agree():
    """Requirement 2: the real-valued sine/cosine form is exact, not approximate."""
    *_, class_index, phi, _, _, r = _problem(n=32, S=16, C=4)
    zc = class_scores_complex(r, phi, class_index, 4)
    zr = class_scores_real(r, phi, class_index, 4)
    assert np.allclose(zc, zr, rtol=0, atol=1e-14)
    # the published historical figure was agreement to ~2.2e-16; require at least this
    assert np.max(np.abs(zc - zr)) < 1e-13


def test_complex_and_real_agree_in_the_model():
    """Requirement 2, at the level of fitted-model predictions."""
    from datasets.generation.synthetic import make, stratified_split
    from qcis import QCISClassifier

    X, y = make("xor", seed=0)
    tr, te = stratified_split(y, seed=0)
    a = QCISClassifier("trained_phase", dim=3, use_real=False).fit(X[tr], y[tr], epochs=40, seed=0)
    b = QCISClassifier("trained_phase", dim=3, use_real=True).fit(X[tr], y[tr], epochs=40, seed=0)
    assert np.allclose(a.decision_function(X[te]), b.decision_function(X[te]), atol=1e-12)


def test_scores_are_finite_and_non_negative():
    """Requirement 3: class scores are finite and non-negative; probabilities sum to 1."""
    for mech in ("coords_only", "incoherent", "fixed_phase", "trained_phase"):
        *_, class_index, phi, _, _, r = _problem()
        z = class_scores(r, phi, class_index, 2, mech)
        assert np.all(np.isfinite(z)), mech
        assert np.all(z >= 0), mech
        P = probabilities(z)
        assert np.all(np.isfinite(P)), mech
        assert np.allclose(P.sum(axis=1), 1.0, atol=1e-12), mech


def test_extreme_distances_are_numerically_stable():
    """Requirement 4: very small and very large distances do not produce NaN or inf."""
    for scale in (1e-12, 1e-6, 1e6, 1e12):
        q = np.zeros((3, 2))
        states = np.array([[scale, 0.0], [0.0, scale], [-scale, 0.0]])
        class_index = np.array([0, 1, 0])
        phi = np.array([0.0, 1.0, 2.0])
        D = squared_distances(q, states)
        r = normalized_magnitudes(gaussian_similarity(D, 1.0))
        z = class_scores_complex(r, phi, class_index, 2)
        P = probabilities(z)
        assert np.all(np.isfinite(r)), scale
        assert np.all(np.isfinite(z)), scale
        assert np.all(np.isfinite(P)), scale
        assert np.all(z >= 0), scale


def test_phase_wrapping_invariance():
    """Requirement 5: z_c is invariant to 2*pi shifts and to a global phase shift."""
    *_, class_index, phi, _, _, r = _problem(n=6, S=8, C=2)
    base = class_scores_complex(r, phi, class_index, 2)

    # adding any multiple of 2*pi to a phase changes nothing
    shifted = phi + 2 * np.pi * RNG.integers(-3, 4, size=len(phi))
    assert np.allclose(base, class_scores_complex(r, shifted, class_index, 2), atol=1e-12)

    # a global phase offset is unobservable: it multiplies every class amplitude by e^{i theta}
    for theta in (0.3, 1.7, np.pi):
        assert np.allclose(base, class_scores_complex(r, phi + theta, class_index, 2), atol=1e-12)


def test_global_phase_invariance_fails_for_relative_phase():
    """The invariance above is global only; relative phase genuinely changes the score."""
    r = np.ones((1, 2)) / np.sqrt(2)
    class_index = np.array([0, 0])
    aligned = class_scores_complex(r, np.array([0.0, 0.0]), class_index, 1)
    opposed = class_scores_complex(r, np.array([0.0, np.pi]), class_index, 1)
    assert aligned[0, 0] > opposed[0, 0] + 1e-6


def test_incoherent_score_equals_squared_sum_of_magnitudes():
    """With all phases zero the score reduces to (sum r_i)^2, as documented."""
    *_, class_index, _, _, _, r = _problem(n=5, S=8, C=2)
    z = class_scores(r, np.zeros(8), class_index, 2, "incoherent")
    expected = np.stack([r[:, class_index == c].sum(1) ** 2 for c in range(2)], axis=1)
    assert np.allclose(z, expected, atol=1e-14)


def test_coords_only_score_equals_sum_of_squared_magnitudes():
    """Ablation A reduces to sum_i r_i^2 per class."""
    *_, class_index, _, _, _, r = _problem(n=5, S=8, C=2)
    z = class_scores(r, np.zeros(8), class_index, 2, "coords_only")
    expected = np.stack([(r[:, class_index == c] ** 2).sum(1) for c in range(2)], axis=1)
    assert np.allclose(z, expected, atol=1e-14)
