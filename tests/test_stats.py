"""The statistical helpers must behave as documented."""

import numpy as np

from qcis import stats


def test_bootstrap_ci_brackets_the_mean():
    rng = np.random.default_rng(0)
    d = rng.normal(0.5, 0.2, size=40)
    ci = stats.paired_bootstrap_ci(d, n_boot=2000, seed=0)
    assert ci["ci_low"] < ci["mean"] < ci["ci_high"]
    assert ci["n"] == 40


def test_bootstrap_is_deterministic():
    d = np.linspace(-1, 1, 25)
    a = stats.paired_bootstrap_ci(d, n_boot=500, seed=7)
    b = stats.paired_bootstrap_ci(d, n_boot=500, seed=7)
    assert a == b


def test_holm_is_monotone_and_bounded():
    p = [0.001, 0.02, 0.04, 0.5]
    adj = stats.holm_adjust(p)
    assert np.all(adj >= np.array(p) - 1e-12)
    assert np.all(adj <= 1.0)
    assert np.all(np.diff(adj[np.argsort(p)]) >= -1e-12)


def test_bh_is_monotone_in_sorted_order():
    p = [0.001, 0.02, 0.04, 0.5]
    adj = stats.bh_adjust(p)
    assert np.all(np.diff(adj[np.argsort(p)]) >= -1e-12)
    assert np.all(adj <= 1.0)


def test_mcnemar_symmetric_case_has_p_one():
    a = np.array([1, 1, 0, 0])
    b = np.array([0, 0, 1, 1])
    assert stats.mcnemar(a, b)["p_value"] == 1.0


def test_mcnemar_detects_a_clear_difference():
    a = np.ones(30, dtype=bool)
    b = np.concatenate([np.ones(15, dtype=bool), np.zeros(15, dtype=bool)])
    assert stats.mcnemar(a, b)["p_value"] < 0.01


def test_family_means_average_seeds_before_comparison():
    rows = [
        {"family": "f1", "mechanism": "m", "accuracy": 0.5},
        {"family": "f1", "mechanism": "m", "accuracy": 1.0},
        {"family": "f2", "mechanism": "m", "accuracy": 0.8},
    ]
    means = stats.family_means(rows)
    assert np.isclose(means[("f1", "m")], 0.75)
    assert np.isclose(means[("f2", "m")], 0.8)
