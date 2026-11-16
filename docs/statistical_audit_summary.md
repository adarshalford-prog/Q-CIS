# Q-CIS — Phase 7 statistical audit

The audit of the Phase 7 results and the corrected inference.

> **Important.** Transcribed from the project's recorded research history. The audit package is
> not published in this release.

---

## 1. Phase 7 statistical audit — corrected inference

The audit reported:
- All 8 integrity checks passed.
- 450 fits, 18 families, complete 5-seed × 5-mechanism grid, no duplicate records.
- Both frozen formula SHA-256 digests recomputed.
- All 90 geometry features reproduced from training split only; feature builders accepted no test data, so structural leakage was ruled out by the audit.
- No near-duplicate families; closest Phase 7 family distance was 2.42 from any of 56 development families.
- Archived correlations reproduced exactly; archived p-values reproduced to machine precision.
- Original paired tests used 90 per-seed observations as independent instead of 18 independent families.

### Family-level corrected comparisons
- Selector versus always-coherent: +0.56 points; 95% CI [−0.59, +1.70], p=.285. No statistically established difference.
- Selector versus RBF: −2.03 points; 95% CI [−7.38, +1.74], p=.552. This is inconclusive, not evidence of equivalence.
- RBF versus always-coherent: original p=.033 became p=.877 at family level.
- Oracle versus RBF: p=.438; not significant and not evidence of equivalence.
- Difference between CV-gap correlation (+.491) and training-gap correlation (+.583): −.092, bootstrap CI [−.322, +.091], Holm p=1.00; no detectable difference.
- CV-gap interval approximately [−.020, +.856], including zero despite asymptotic p=.038.
- Selector classified mechanism choice on 16/18 families. Exact interval reported as 65.3–98.6%, p=.0013 versus chance. Majority-choice baseline was 8/18.
- Selector versus always-incoherent: +1.96 points, family-level p=.028; this was the only paired contrast distinguishable from zero in the audit before considering further multiplicity adjustment.
- Selector halved regret of majority choice: 0.51 points versus 1.08 points.
- Audit interpretation: a valid mechanism classifier on this evaluation bank, but not an established useful mechanism selector; practical utility remains small and uncertain.
- High-dimensional subgroup mean −1.31 points, CI [−4.26, +1.80]; four harmful, zero neutral, two beneficial. Within-subgroup correlation −.314 with very wide CI approximately [−.90, +.55]. Correlation-difference permutation p=.035, but power concerns led to exploratory/inconclusive status.

### Correct statistical interpretation

The family, not each seed-level fit, is the independent unit for the relevant generalization claim. The corrected selector-vs-always-coherent result does not establish a reliable improvement. The selector-vs-RBF result is inconclusive and cannot be described as a tie or equivalence. The selector's 16/18 mechanism-choice accuracy is a descriptive classification result; it does not automatically prove practical value.

---
