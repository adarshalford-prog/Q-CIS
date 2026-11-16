# Q-CIS benchmark summary — reference implementation 0.2.0

Generated from `fits.csv`.

> **What this is.** Output of the reference implementation in `src/qcis`, run on freshly generated synthetic families. It is **not** a reproduction of the historical Phase 1–7 figures, whose code, data and configurations were never published. See `REPOSITORY_AUDIT.md`.

**Independent unit:** dataset family (seeds averaged within family)  
**Fits:** 176  
**Families:** 8


## Family-level means (test accuracy)

| Family | baseline_nearest_centroid | baseline_rbf_ridge | coords_only | fixed_phase | incoherent | trained_phase |
|---|---|---|---|---|---|---|
| blobs | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| circles | 0.508 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| moons | 0.792 | 0.983 | 0.973 | 0.982 | 0.982 | 0.983 |
| overlapping_clusters | 0.758 | 0.725 | 0.723 | 0.717 | 0.708 | 0.715 |
| rings | 0.483 | 0.825 | 0.817 | 0.810 | 0.793 | 0.762 |
| shells | 0.542 | 0.917 | 0.613 | 0.642 | 0.630 | 0.652 |
| spirals | 0.742 | 0.833 | 0.905 | 0.897 | 0.913 | 0.888 |
| xor | 0.400 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| **mean** | **0.653** | **0.910** | **0.879** | **0.881** | **0.878** | **0.875** |

## Paired family-level contrasts

| Contrast | Mean diff (pp) | 95% CI (pp) | p | p (Holm) | Distinguishable from zero |
|---|---|---|---|---|---|
| trained_phase - incoherent | -0.33 | [-1.48, +0.71] | 0.5804 | 1.0000 | no |
| trained_phase - coords_only | -0.40 | [-2.15, +1.23] | 0.6658 | 1.0000 | no |
| trained_phase - fixed_phase | -0.58 | [-1.90, +0.27] | 0.3876 | 1.0000 | no |
| incoherent - coords_only | -0.06 | [-0.94, +0.73] | 0.9542 | 1.0000 | no |
| trained_phase - baseline_rbf_ridge | -3.54 | [-10.83, +1.27] | 0.2584 | 1.0000 | no |
| trained_phase - baseline_nearest_centroid | +22.19 | [+8.27, +37.17] | 0.0006 | 0.0036 | yes |

A contrast that is not distinguishable from zero is **inconclusive**. It is not evidence of equivalence.


## Geometry gap vs measured phase benefit

Spearman rho = 0.0238 over 8 families (descriptive only).

| Family | cv_gap | phase benefit (pp) |
|---|---|---|
| blobs | +0.0179 | +0.00 |
| circles | +0.4679 | +0.00 |
| moons | +0.1500 | +0.17 |
| overlapping_clusters | +0.0071 | +0.67 |
| rings | +0.2714 | -3.17 |
| shells | +0.2929 | +2.17 |
| spirals | +0.0321 | -2.50 |
| xor | +0.4571 | +0.00 |

## Frozen selectors

| Selector | Correct | Comparable families | Accuracy |
|---|---|---|---|
| D1 | 3 | 5 | 0.6 |
| D2 | 3 | 5 | 0.6 |

D1 and D2 are the two frozen formulas whose constants are published. D3 is not implemented because its threshold and corrected polarity are not recorded in the published material. These numbers exercise the selector mechanism on newly generated data; they do not reproduce the historical selector results.
