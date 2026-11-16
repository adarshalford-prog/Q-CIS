"""Frozen mechanism selectors from the historical record.

These are the two frozen formulas whose constants are published in
``docs/statistical_audit_summary.md`` and ``docs/phase_history.md``:

    D1: a decision stump on ``cv_gap`` with threshold 0.0727.
        If cv_gap > 0.0727 -> use coherent phases; otherwise -> incoherent.
        The default is therefore "off" (incoherent), which is why the historical
        audit notes the stump got most harmful families right simply by defaulting
        to off.

    D2: a least-squares line  Delta = 0.0144 + 0.2592 * cv_gap,
        where Delta is the predicted phase benefit in percentage points.
        Use coherent phases when Delta > 0.

A third frozen formula, D3 (a stump on the cross-validated linear probe), is
described in the record as having had its polarity corrected before evaluation,
but neither its threshold nor its corrected polarity is recorded in the published
material. It is therefore **not** implemented here. Inventing a threshold would
mean fabricating part of the historical method, which this release does not do.

Applying these formulas to newly generated data exercises the *mechanism* of the
selectors. It does not reproduce the historical selector results.
"""

from __future__ import annotations

import numpy as np

D1_THRESHOLD = 0.0727
D2_INTERCEPT = 0.0144
D2_SLOPE = 0.2592


def d1_stump(cv_gap):
    """Frozen D1: coherent phases when ``cv_gap`` exceeds 0.0727, else incoherent."""
    g = np.asarray(cv_gap, dtype=float)
    return np.where(g > D1_THRESHOLD, "trained_phase", "incoherent")


def d2_line_predicted_benefit(cv_gap):
    """Frozen D2: predicted phase benefit in percentage points."""
    return D2_INTERCEPT + D2_SLOPE * np.asarray(cv_gap, dtype=float)


def d2_line(cv_gap):
    """Frozen D2 decision: coherent phases when the predicted benefit is positive."""
    return np.where(d2_line_predicted_benefit(cv_gap) > 0, "trained_phase", "incoherent")


SELECTORS = {"D1": d1_stump, "D2": d2_line}
