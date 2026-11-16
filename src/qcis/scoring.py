"""Score computation for the Q-CIS classical coordinate-and-phase classifier.

These functions implement, literally, the formulation published in
``MATHEMATICAL_MODEL.md`` (the "later classifier formulation" section):

    D_i   = ||q(x) - s_i||^2
    K_i   = exp(-D_i / (2 sigma^2))
    r_i   = sqrt(K_i) / sqrt(sum_j K_j)              so that  sum_i r_i^2 = 1
    a_i   = r_i * exp(i * phi_i)
    z_c   = |sum_{i in I_c} a_i|^2
    P(c)  = z_c / sum_k z_k

The real-valued equivalent used by :func:`class_scores_real` is

    z_c = (sum_{i in I_c} r_i cos phi_i)^2 + (sum_{i in I_c} r_i sin phi_i)^2

which is exact, not an approximation. Complex arithmetic is therefore not required
to compute the score.

Nothing here is quantum. All quantities are ordinary real numbers on a classical
computer; "quantum-inspired" refers only to the shape of the mathematics.
"""

from __future__ import annotations

import numpy as np

# A floor applied to the Gaussian similarities before the square root, purely to keep
# sqrt() and the log-domain stable at extreme distances. It is far below any value that
# affects float64 results in practice.
_K_FLOOR = 1e-300


def squared_distances(q: np.ndarray, states: np.ndarray) -> np.ndarray:
    """Squared Euclidean distance between every query and every state.

    Parameters
    ----------
    q : (B, d) array of query coordinates
    states : (S, d) array of state coordinates

    Returns
    -------
    (B, S) array of squared distances
    """
    q = np.atleast_2d(np.asarray(q, dtype=float))
    states = np.asarray(states, dtype=float)
    diff = q[:, None, :] - states[None, :, :]
    return np.einsum("bsd,bsd->bs", diff, diff)


def gaussian_similarity(D: np.ndarray, sigma: float) -> np.ndarray:
    """K_i = exp(-D_i / (2 sigma^2)), floored away from exact zero."""
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    K = np.exp(-np.asarray(D, dtype=float) / (2.0 * sigma * sigma))
    return np.maximum(K, _K_FLOOR)


def normalized_magnitudes(K: np.ndarray) -> np.ndarray:
    """r_i = sqrt(K_i) / sqrt(sum_j K_j).

    By construction ``sum_i r_i^2 == 1`` for every row. This is asserted in
    ``tests/test_scoring.py``.
    """
    K = np.atleast_2d(np.asarray(K, dtype=float))
    num = np.sqrt(K)
    den = np.sqrt(K.sum(axis=1, keepdims=True))
    return num / den


def _group_sum(values: np.ndarray, class_index: np.ndarray, n_classes: int) -> np.ndarray:
    """Sum ``values`` (B, S) over the states belonging to each class -> (B, C)."""
    values = np.atleast_2d(values)
    out = np.zeros((values.shape[0], n_classes), dtype=values.dtype)
    for c in range(n_classes):
        mask = class_index == c
        if np.any(mask):
            out[:, c] = values[:, mask].sum(axis=1)
    return out


def class_scores_complex(
    r: np.ndarray, phi: np.ndarray, class_index: np.ndarray, n_classes: int
) -> np.ndarray:
    """z_c = |sum_{i in I_c} r_i exp(i phi_i)|^2, computed with complex arithmetic."""
    r = np.atleast_2d(np.asarray(r, dtype=float))
    phi = np.asarray(phi, dtype=float)
    amp = r * np.exp(1j * phi)[None, :]
    A = _group_sum(amp, class_index, n_classes)
    return (A.real ** 2 + A.imag ** 2)


def class_scores_real(
    r: np.ndarray, phi: np.ndarray, class_index: np.ndarray, n_classes: int
) -> np.ndarray:
    """The same z_c, computed with only real arithmetic."""
    r = np.atleast_2d(np.asarray(r, dtype=float))
    phi = np.asarray(phi, dtype=float)
    X = _group_sum(r * np.cos(phi)[None, :], class_index, n_classes)
    Y = _group_sum(r * np.sin(phi)[None, :], class_index, n_classes)
    return X * X + Y * Y


def class_scores_coords_only(
    r: np.ndarray, class_index: np.ndarray, n_classes: int
) -> np.ndarray:
    """Ablation A: coordinates only, no interference. z_c = sum_{i in I_c} r_i^2."""
    r = np.atleast_2d(np.asarray(r, dtype=float))
    return _group_sum(r * r, class_index, n_classes)


def class_scores(
    r: np.ndarray,
    phi: np.ndarray,
    class_index: np.ndarray,
    n_classes: int,
    mechanism: str = "trained_phase",
    use_real: bool = False,
) -> np.ndarray:
    """Dispatch to the class-score variant selected by ``mechanism``.

    ``mechanism`` is one of the values in :data:`qcis.model.MECHANISMS`.
    """
    if mechanism == "coords_only":
        return class_scores_coords_only(r, class_index, n_classes)
    if use_real:
        return class_scores_real(r, phi, class_index, n_classes)
    return class_scores_complex(r, phi, class_index, n_classes)


def probabilities(z: np.ndarray) -> np.ndarray:
    """P(c) = z_c / sum_k z_k, guarded against a zero denominator."""
    z = np.atleast_2d(np.asarray(z, dtype=float))
    total = z.sum(axis=1, keepdims=True)
    total = np.where(total > 0, total, 1.0)
    return z / total
