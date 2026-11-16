"""The Q-CIS classifier: a classical coordinate-and-phase model.

This is a reference implementation of the equations published in
``MATHEMATICAL_MODEL.md``. It is not the original research code and does not
reproduce the Phase 1-7 figures.

Model
-----
An input ``x`` is mapped to a query coordinate ``q = W x`` (a learned linear
encoder). Each internal state ``i`` has a coordinate ``s_i`` and a phase
``phi_i``, and belongs to exactly one class. Distances feed a Gaussian
similarity, similarities are normalised into magnitudes ``r_i`` with
``sum_i r_i^2 = 1``, and class scores are the squared modulus of the summed
amplitudes ``r_i exp(i phi_i)`` over the states of that class.

Everything is ordinary real arithmetic on a CPU. No quantum state, no
entanglement, and no quantum advantage is involved or claimed.

Ablation mechanisms
-------------------
===============  ==========================================================
``coords_only``  z_c = sum_{i in I_c} r_i^2. No interference at all.
``incoherent``   phases fixed at zero, so z_c = (sum_{i in I_c} r_i)^2.
``fixed_phase``  phases drawn once at random and then held fixed.
``trained_phase`` phases are learned alongside coordinates and encoder.
===============  ==========================================================

These correspond to the ablation variants A-F in the original proposal
(coordinates only; coordinates + fixed phases; coordinates + trainable phases;
coordinates + interference without phase learning; coordinates + feedback-based
phase learning; full Q-CIS).
"""

from __future__ import annotations

import numpy as np

from .scoring import (
    class_scores,
    gaussian_similarity,
    normalized_magnitudes,
    probabilities,
    squared_distances,
)

MECHANISMS = ("coords_only", "incoherent", "fixed_phase", "trained_phase")

_MECHANISM_DOC = {
    "coords_only": "Ablation A - coordinates only, no interference.",
    "incoherent": "Ablation D - interference with all phases fixed at zero.",
    "fixed_phase": "Ablation B - interference with random phases held fixed.",
    "trained_phase": "Ablations C/E/F - phases learned with the coordinates.",
}


class QCISClassifier:
    """Classical coordinate-and-phase classifier.

    Parameters
    ----------
    mechanism : str
        One of :data:`MECHANISMS`.
    n_states_per_class : int
        Number of internal states allocated to each class. State-to-class
        membership is fixed at construction from training labels only.
    dim : int
        Dimensionality ``d`` of the coordinate space.
    use_real : bool
        If True, evaluate class scores with the real-valued sine/cosine
        equivalent instead of complex arithmetic. The two agree to machine
        precision; see ``tests/test_scoring.py``.
    """

    def __init__(
        self,
        mechanism: str = "trained_phase",
        n_states_per_class: int = 8,
        dim: int = 4,
        use_real: bool = False,
    ):
        if mechanism not in MECHANISMS:
            raise ValueError(f"mechanism must be one of {MECHANISMS}, got {mechanism!r}")
        self.mechanism = mechanism
        self.n_states_per_class = int(n_states_per_class)
        self.dim = int(dim)
        self.use_real = bool(use_real)

    # ------------------------------------------------------------------ init
    def _init_params(self, X, y, rng):
        n, D = X.shape
        classes = np.unique(y)
        self.classes_ = classes
        C = len(classes)

        self.W_ = rng.normal(0.0, 1.0 / np.sqrt(D), size=(D, self.dim))

        # state-to-class membership, from training labels only
        idx = np.repeat(classes, self.n_states_per_class)
        self.class_index_ = np.searchsorted(classes, idx).astype(int)

        q = X @ self.W_
        S = len(self.class_index_)
        states = np.empty((S, self.dim), dtype=float)
        for c in range(C):
            mask_c = self.class_index_ == c
            qc = q[y == classes[c]]
            centre = qc.mean(axis=0) if len(qc) else np.zeros(self.dim)
            k = int(mask_c.sum())
            states[mask_c] = centre + rng.normal(0.0, 0.3, size=(k, self.dim))
        self.states_ = states

        # phases
        if self.mechanism == "incoherent" or self.mechanism == "coords_only":
            self.phi_ = np.zeros(S)
        else:
            self.phi_ = rng.uniform(-np.pi, np.pi, size=S)

        # bandwidth from the median training distance (a deterministic heuristic)
        Dq = squared_distances(q, self.states_)
        med = float(np.median(Dq))
        sigma0 = np.sqrt(max(med, 1e-6) / (2.0 * np.log(2.0)))
        self.log_sigma_ = float(np.log(sigma0))

    # --------------------------------------------------------------- forward
    def _forward(self, X):
        q = X @ self.W_
        D = squared_distances(q, self.states_)
        sigma = float(np.exp(self.log_sigma_))
        K = gaussian_similarity(D, sigma)
        S_sum = K.sum(axis=1)
        r = normalized_magnitudes(K)
        C = len(self.classes_)

        if self.mechanism == "coords_only":
            z = class_scores(r, self.phi_, self.class_index_, C, "coords_only")
            Xc = Yc = None
        else:
            phi = np.zeros_like(self.phi_) if self.mechanism == "incoherent" else self.phi_
            z = class_scores(
                r, phi, self.class_index_, C, self.mechanism, use_real=self.use_real
            )
            cos_p, sin_p = np.cos(phi), np.sin(phi)
            Xc = np.zeros((X.shape[0], C))
            Yc = np.zeros((X.shape[0], C))
            for c in range(C):
                m = self.class_index_ == c
                if np.any(m):
                    Xc[:, c] = (r[:, m] * cos_p[m][None, :]).sum(axis=1)
                    Yc[:, c] = (r[:, m] * sin_p[m][None, :]).sum(axis=1)

        P = probabilities(z)
        return {
            "q": q, "D": D, "K": K, "S_sum": S_sum, "r": r,
            "z": z, "P": P, "Xc": Xc, "Yc": Yc, "sigma": sigma,
        }

    def decision_function(self, X):
        return self._forward(self._check_X(X))["z"]

    def predict_proba(self, X):
        return self._forward(self._check_X(X))["P"]

    def predict(self, X):
        P = self.predict_proba(X)
        return self.classes_[np.argmax(P, axis=1)]

    def _check_X(self, X):
        X = np.atleast_2d(np.asarray(X, dtype=float))
        if not hasattr(self, "mean_"):
            return X
        return (X - self.mean_) / self.scale_

    # --------------------------------------------------------------- fitting
    def _loss_and_grads(self, X, y_enc):
        """Cross-entropy loss and its analytic gradients.

        Gradient derivation (all terms finite, no division by K):

            L      = -log P(y) = -log z_y + log Z
            dL/dz_c = 1/Z - [c == y]/z_y

        With ``a_i = dL/dr_i`` and ``S = sum_j K_j``, note that ``r_j`` depends on
        ``D_i`` for *every* j, not only j == i, because ``D_i`` moves the shared
        normaliser ``S``. Writing ``Q = sum_j a_j r_j`` the total derivative is

            dL/dD_i = -(a_i r_i) / (4 sigma^2) + K_i Q / (4 sigma^2 S)

        Using only the i-th term here is a common and silent bug; it makes the
        gradient wrong by a state-dependent factor. ``tests/test_gradients.py``
        checks the full expression against finite differences.

            dD_i/dq = 2(q - s_i),   dD_i/ds_i = -2(q - s_i)
            dL/dsigma = (1/(2 sigma^3)) sum_j a_j r_j D_j (1 - K_j / S)
        """
        f = self._forward(X)
        r, K, D, S_sum, z, P = f["r"], f["K"], f["D"], f["S_sum"], f["z"], f["P"]
        sigma = f["sigma"]
        B = X.shape[0]
        C = len(self.classes_)
        eps = 1e-12

        Z = z.sum(axis=1, keepdims=True)
        z_y = z[np.arange(B), y_enc][:, None]
        loss = float(np.mean(-np.log(np.maximum(z_y / np.maximum(Z, eps), eps))))

        onehot = np.zeros_like(z)
        onehot[np.arange(B), y_enc] = 1.0
        g = 1.0 / np.maximum(Z, eps) - onehot / np.maximum(z_y, eps)  # dL/dz

        gc = g[:, self.class_index_]  # (B, S) gradient for each state's own class

        if self.mechanism == "coords_only":
            dL_dr = 2.0 * r * gc
            dL_dphi = np.zeros_like(r)
        else:
            U = 2.0 * gc * f["Xc"][:, self.class_index_]
            V = 2.0 * gc * f["Yc"][:, self.class_index_]
            cos_p = np.cos(self.phi_)[None, :]
            sin_p = np.sin(self.phi_)[None, :]
            dL_dr = U * cos_p + V * sin_p
            dL_dphi = r * (V * cos_p - U * sin_p)

        # Total derivative dL/dD_i. Every r_j depends on D_i through the shared
        # normaliser S = sum_j K_j, so the cross terms must be included.
        a = dL_dr                                    # (B, S), un-averaged
        Q = (a * r).sum(axis=1, keepdims=True)       # (B, 1)
        denom = 4.0 * sigma * sigma
        dL_dD = -(a * r) / denom + K * Q / (denom * S_sum[:, None])  # (B, S)

        diff = f["q"][:, None, :] - self.states_[None, :, :]  # (B, S, d)
        dL_dq = 2.0 * np.einsum("bs,bsd->bd", dL_dD, diff) / B
        dL_ds = -2.0 * np.einsum("bs,bsd->sd", dL_dD, diff) / B

        # Bandwidth derivative. S = sum_i K_i depends on sigma through every state,
        # so the normaliser contributes a full sum, not the single K_j term:
        #   dL/dsigma = (1/(2 sigma^3)) [ sum_j a_j r_j D_j
        #                                 - (sum_j a_j r_j)(sum_i K_i D_i)/S ]
        Qb = (a * r).sum(axis=1)
        P1 = (a * r * D).sum(axis=1)
        R = (K * D).sum(axis=1)
        dL_dsigma = float(np.sum((1.0 / (2.0 * sigma ** 3)) * (P1 - Qb * R / S_sum))) / B
        dL_dlog_sigma = dL_dsigma * sigma

        dL_dW = X.T @ dL_dq

        # Phases are structurally absent for coords_only (no interference at all) and
        # pinned to zero for incoherent, so their gradient is genuinely zero there.
        # For fixed_phase the gradient is real but is simply not applied by `fit`.
        if self.mechanism in ("coords_only", "incoherent"):
            dL_dphi = np.zeros_like(self.phi_)
        else:
            dL_dphi = dL_dphi.mean(axis=0)

        return loss, {
            "W": dL_dW,
            "states": dL_ds,
            "phi": dL_dphi,
            "log_sigma": np.array(dL_dlog_sigma),
        }

    def fit(self, X, y, epochs=200, lr=0.05, seed=0, verbose=False):
        """Train with Adam on the cross-entropy loss.

        Deterministic given ``seed``: identical inputs and seed produce bit-identical
        parameters and predictions (asserted in ``tests/test_determinism.py``).
        Feature standardisation uses training statistics only.
        """
        X = np.atleast_2d(np.asarray(X, dtype=float))
        y = np.asarray(y)

        self.mean_ = X.mean(axis=0)
        self.scale_ = X.std(axis=0)
        self.scale_[self.scale_ < 1e-12] = 1.0
        Xs = (X - self.mean_) / self.scale_

        rng = np.random.default_rng(seed)
        self._init_params(Xs, y, rng)
        y_enc = np.searchsorted(self.classes_, y)

        params = ["W", "states", "phi", "log_sigma"]
        m = {k: np.zeros_like(getattr(self, f"{k}_")) for k in params}
        v = {k: np.zeros_like(getattr(self, f"{k}_")) for k in params}
        b1, b2, eps = 0.9, 0.999, 1e-8
        trainable = {"W", "states", "log_sigma"}
        if self.mechanism == "trained_phase":
            trainable.add("phi")

        self.history_ = []
        for t in range(1, epochs + 1):
            loss, grads = self._loss_and_grads(Xs, y_enc)
            self.history_.append(loss)
            for k in params:
                if k not in trainable:
                    continue
                grad = grads[k]
                m[k] = b1 * m[k] + (1 - b1) * grad
                v[k] = b2 * v[k] + (1 - b2) * grad * grad
                mhat = m[k] / (1 - b1 ** t)
                vhat = v[k] / (1 - b2 ** t)
                upd = lr * mhat / (np.sqrt(vhat) + eps)
                setattr(self, f"{k}_", getattr(self, f"{k}_") - upd)
            if self.mechanism == "trained_phase":
                self.phi_ = np.mod(self.phi_ + np.pi, 2 * np.pi) - np.pi
            if verbose and t % max(1, epochs // 10) == 0:
                print(f"  epoch {t:4d}  loss {loss:.6f}")
        return self

    # ------------------------------------------------------------- utilities
    @property
    def n_states(self):
        return len(self.class_index_)

    @property
    def n_trainable_parameters(self):
        return int(self.W_.size + self.states_.size + (self.n_states if self.mechanism == "trained_phase" else 0) + 1)

    def score(self, X, y):
        return float(np.mean(self.predict(X) == np.asarray(y)))

    def __repr__(self):
        return (
            f"QCISClassifier(mechanism={self.mechanism!r}, dim={self.dim}, "
            f"n_states_per_class={self.n_states_per_class})"
        )
