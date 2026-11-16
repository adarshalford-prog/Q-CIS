"""Q-CIS reference implementation.

This package implements the *published* mathematical formulation of Q-CIS: the
classical coordinate-and-phase classifier described in ``MATHEMATICAL_MODEL.md``.

It is a reference implementation written from the published equations. It is NOT
the original research code used to produce the Phase 1-7 numbers reported in
``RESULTS_SUMMARY.md``, and it does not reproduce those numbers. See
``REPOSITORY_AUDIT.md`` for the provenance of each artefact in this repository.
"""

from .scoring import (
    squared_distances,
    gaussian_similarity,
    normalized_magnitudes,
    class_scores_complex,
    class_scores_real,
    class_scores,
    probabilities,
)
from .model import QCISClassifier, MECHANISMS

__version__ = "0.2.0"

__all__ = [
    "squared_distances",
    "gaussian_similarity",
    "normalized_magnitudes",
    "class_scores_complex",
    "class_scores_real",
    "class_scores",
    "probabilities",
    "QCISClassifier",
    "MECHANISMS",
    "__version__",
]
