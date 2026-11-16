# Q-CIS — Reported results

Headline results across Phases 1–7, with the corrected Phase 7 statistical audit.

> **Important.** Every figure below is **transcribed from the project's recorded research
> history**. The raw fit-level data, code, and analysis scripts are not included in this release,
> so these numbers have not been independently recalculated here. Treat them as author-reported.
> The full phase-by-phase record is in [docs/phase_history.md](docs/phase_history.md) and the
> audit in [docs/statistical_audit_summary.md](docs/statistical_audit_summary.md).

## Headline figures

| Phase | What was measured | Reported result |
|---|---|---|
| 1 — Initial prototype | Q-CIS coordinate-only accuracy, Study 1 (5 seeds × 4 datasets) | XOR 94.8 · Circles 99.0 · Overlap 69.6 · Spirals 82.5 |
| 1 — Initial prototype | Trained vs fixed-random phase, Study 2 (1,120 fits) | +0.14 pp, CI approx. −0.01 to +0.28, p = .074; 88/120 paired units identical |
| 3 — Independent reproduction | Reproduction fidelity | 36/36 model-dataset cells bit-for-bit identical |
| 3 — Independent reproduction | Aggregate comparison | Behind RBF by 3.33 pp (BH-adjusted p = .010); behind SVM by 2.89 pp (BH-adjusted p = .026) |
| 3 — Independent reproduction | Runtime at 100 states | Q-CIS training 0.80 s, 17 ms/1000 queries; RBF 0.10 s |
| 4 — Mechanism and stability | Real vs complex implementation | Matched to approx. $2.2\times10^{-16}$; real-valued version about 3% faster |
| 4 — Mechanism and stability | 13 datasets | Tied RBF/SVM overall; lost by 14 pp on four concentric-rings experiments |
| 5 — Geometry and selection | Nonlinear-minus-linear probe gap vs phase benefit | rho = +.759, BH-adjusted p < .0001 |
| 5 — Geometry and selection | First selector, held-out 12 parameterisations | 7/12 = 58.3%, binomial p = .774; no gain over always-coherent |
| 6 — Independent geometry validation | Frozen stump mechanism choice, 24 new families / 600 fits | 19/20 non-tie families correct (95%, p < .0001); disabled phases on all four harmful families |
| 6 — Independent geometry validation | Gap replication | rho = +.772, p < .0001 |
| 6 — Independent geometry validation | Overall standing | Behind RBF by 4.34 pp, SVM by 4.17 pp, MLP by 2.29 pp |
| 7 — Cross-validated geometry | Frozen D1 selector, new bank (18 families, 450 fits) | 16/18 (88.9%, p = .0013) mechanism-choice accuracy |
| 7 — Cross-validated geometry | Policy accuracy | Selector 84.44% vs always-coherent 84.39%; RBF 86.47% |
| 7 audit — corrected inference | Selector vs always-coherent, family level | +0.56 pp, 95% CI [−0.59, +1.70], p = .285 — not statistically established |
| 7 audit — corrected inference | Selector vs RBF, family level | −2.03 pp, 95% CI [−7.38, +1.74], p = .552 — inconclusive, not equivalence |

## Consolidated interpretation

## 21. What the evidence supports

The reported experiments support cautious statements that:
- A classical coordinate-and-phase classifier was implemented and tested on multiple synthetic dataset families.
- The squared-modulus score has an exact real-valued sine/cosine equivalent in the tested formulation.
- Phase effects are dataset-dependent and can be unstable.
- A nonlinear-minus-linear geometry probe gap showed associations with phase benefit in multiple reported experimental banks.
- A frozen selector classified mechanism choice well on some later evaluation banks.
- The corrected Phase 7 evidence does not establish a reliable practical gain over always-coherent phases.
- Q-CIS did not demonstrate consistent superiority over conventional RBF, SVM, or MLP baselines.

## 22. What the evidence does not support

Do not claim:
- Quantum advantage or physical quantum computation.
- Entanglement or actual quantum superposition.
- A new computational primitive.
- General superiority over RBF, SVM, MLP, or neural networks.
- A reliable practical benefit from the Phase 7 selector over always-coherent phases.
- Equivalence between the selector and RBF based on a nonsignificant comparison.
- General-purpose AI, long-term memory, or reasoning capabilities.
- Independent reproducibility from this release dossier alone.

## Phase 7 statistical audit — summary

The audit reported:
- All 8 integrity checks passed.
- 450 fits, 18 families, complete 5-seed × 5-mechanism grid, no duplicate records.
- Both frozen formula SHA-256 digests recomputed.
- All 90 geometry features reproduced from training split only; feature builders accepted no test data, so structural leakage was ruled out by the audit.
- No near-duplicate families; closest Phase 7 family distance was 2.42 from any of 56 development families.
- Archived correlations reproduced exactly; archived p-values reproduced to machine precision.
- Original paired tests used 90 per-seed observations as independent instead of 18 independent families.

The audit's central correction is that **the dataset family, not each seed-level fit, is the
independent unit** for the relevant generalisation claim. Read against that unit:

- Selector versus always-coherent: no statistically established difference (p = .285).
- Selector versus RBF: inconclusive — this is not evidence of equivalence.
- Selector versus always-incoherent: +1.96 pp, family-level p = .028 — the only paired contrast
  distinguishable from zero in the audit before further multiplicity adjustment.
- Selector halved regret of the majority choice: 0.51 pp versus 1.08 pp.

The audit's own conclusion: a valid **mechanism classifier** on this evaluation bank, but not an
established useful **mechanism selector**; practical utility remains small and uncertain.

---

## Further reading

- Full phase record: [docs/phase_history.md](docs/phase_history.md)
- Full audit detail: [docs/statistical_audit_summary.md](docs/statistical_audit_summary.md)
- Limitations: [LIMITATIONS.md](LIMITATIONS.md)
