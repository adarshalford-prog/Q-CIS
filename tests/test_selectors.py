"""The frozen selectors must implement the published constants exactly."""

import numpy as np

from qcis import selectors


def test_d1_threshold_is_the_published_value():
    assert selectors.D1_THRESHOLD == 0.0727


def test_d1_switches_at_the_threshold():
    assert selectors.d1_stump([0.0727 - 1e-9])[0] == "incoherent"
    assert selectors.d1_stump([0.0727 + 1e-9])[0] == "trained_phase"


def test_d1_defaults_to_off_for_negative_gap():
    assert selectors.d1_stump([-0.5, 0.0])[0] == "incoherent"
    assert selectors.d1_stump([-0.5, 0.0])[1] == "incoherent"


def test_d2_coefficients_are_the_published_values():
    assert selectors.D2_INTERCEPT == 0.0144
    assert selectors.D2_SLOPE == 0.2592
    assert np.isclose(selectors.d2_line_predicted_benefit(0.0), 0.0144)


def test_d2_zero_crossing():
    # Delta = 0 at cv_gap = -0.0144 / 0.2592
    x = -0.0144 / 0.2592
    assert selectors.d2_line([x - 1e-6])[0] == "incoherent"
    assert selectors.d2_line([x + 1e-6])[0] == "trained_phase"


def test_d3_is_documented_as_not_implemented():
    assert set(selectors.SELECTORS) == {"D1", "D2"}
