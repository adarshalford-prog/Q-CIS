# Repository audit

An honest account of what this repository contained before the v0.2.0 release, what
was missing, what has been added, and what can and cannot be reproduced. Written by
inspecting every tracked file and the full commit history, not by trusting the
documentation's description of the code.

## Method

* `git ls-files` and a full `git log --stat` on `main` at commit `cbc40c0`.
* Every one of the tracked files read in full.
* Every numeric claim in the documentation checked against the document it came from.
* No assumption that the documentation described code that was actually present.

## What existed before v0.2.0

Twelve tracked files, all prose or metadata. **No executable file of any kind.**

| Path | Kind | Notes |
|---|---|---|
| `README.md` | docs | Overview and partial-release statement |
| `LICENSE` | metadata | MIT, but the copyright line carried an inconsistent attribution string |
| `CITATION.cff` | metadata | Declared `type: software` although the repository contained no software |
| `RESEARCH_SUMMARY.md` | docs | Motivation, questions, interpretation |
| `MATHEMATICAL_MODEL.md` | docs | The equations |
| `METHODOLOGY.md` | docs | Protocol and prototype spec |
| `RESULTS_SUMMARY.md` | docs | Author-reported Phase 1–7 figures |
| `LIMITATIONS.md` | docs | Risks and open questions |
| `docs/original_proposal.md` | docs | Part I in full |
| `docs/phase_history.md` | docs | Phases 1–7 as recorded |
| `docs/statistical_audit_summary.md` | docs | Phase 7 audit |
| `docs/release_dossier.md` | docs | The complete dossier |

Commit history was three commits: an initial commit adding `LICENSE` and a two-line
`README.md`, one commit adding the documentation split, and one fixing a link anchor.
No experiment was ever committed.

## What was missing

| Missing item | Why it matters | Status |
|---|---|---|
| Original implementation source | The central artefact. Nothing could be executed. | **Still missing.** Not published. |
| Dataset generation scripts | Data behind every reported number | **Still missing.** Not published. |
| Exact experiment configurations | Hyperparameters, state counts, dimensions | **Still missing.** Not published. |
| Random seeds used for the historical runs | Without them, exact reruns are impossible | **Still missing.** Not published. |
| Train/validation/test split definitions | Determines what any accuracy figure means | **Still missing.** Not published. |
| Baseline implementations and tuning | The "behind RBF by 3.33 points" claims rest on these | **Still missing.** Not published. |
| Raw fit-level result files | Required to recompute any statistic | **Still missing.** Not published. |
| Statistical analysis scripts | Required to reproduce CIs and p-values | **Still missing.** Not published. |
| Phase 7 audit scripts and outputs | Required to reproduce the audit | **Still missing.** Not published. |
| Dependency versions of the original environment | Numerical results depend on them | **Still missing.** Not published. |
| `requirements.txt` / `pyproject.toml` | Nothing to install | **Added** in v0.2.0 (for this release's code) |
| Any test | No mathematical property was checked | **Added** in v0.2.0 |
| Any CI | No automated verification | **Added** in v0.2.0 (smoke tests) |
| `REPRODUCIBILITY.md` | No instructions for an outside researcher | **Added** in v0.2.0 |

## What v0.2.0 adds

| Path | What it is |
|---|---|
| `src/qcis/scoring.py` | The published score equations, complex and real-valued forms |
| `src/qcis/model.py` | The classifier, with analytic gradients for all four mechanisms |
| `src/qcis/features.py` | Cross-validated geometry probes (this release's own definition) |
| `src/qcis/selectors.py` | The frozen D1 and D2 formulas with their published constants |
| `src/qcis/stats.py` | Paired bootstrap CIs, Holm and BH correction, McNemar, family aggregation |
| `src/qcis/baselines.py` | Nearest-centroid and Gaussian-kernel ridge reference points |
| `datasets/generation/synthetic.py` | Eight deterministic synthetic families |
| `experiments/run_benchmark.py` | Benchmark runner, one CSV row per fit |
| `analysis/audit.py` | Family-level statistical analysis |
| `scripts/run_reproduction.py` | The one-command reproduction |
| `scripts/verify_results.py` | Comparison against the committed reference output |
| `tests/` | 56 tests: mathematics, gradients, determinism, leakage, commands |
| `.github/workflows/ci.yml` | CI: install, test, tiny smoke benchmark |
| `results/reference/` | Committed reference output of the reference implementation |

### Critical provenance note

**`src/qcis` is a reference implementation written from the published equations. It is
not the original research code.** It was written for this release, from
`MATHEMATICAL_MODEL.md`, precisely because the original code was unavailable. It
reproduces the mathematics. It does **not** reproduce the historical results, and it
was not tuned to do so.

The same applies to `datasets/generation/synthetic.py`: same *families* as described,
not the same generators. And to `src/qcis/baselines.py`: the historical baselines are
unavailable, so these are simple stand-ins that must not be used to check the
historical "behind RBF by X points" claims.

## What can genuinely be reproduced

1. **Every mathematical property** of the score function: normalisation
   ($$\sum_i r_i^2 = 1$$), the exact complex/real equivalence, non-negativity and
   finiteness, numerical stability at extreme distances, global phase invariance and
   2π wrapping.
2. **Every gradient** against finite differences, for all four mechanisms, including
   the cross terms through the shared normaliser.
3. **The full benchmark** on the documented synthetic families, deterministically,
   matching a committed reference output to $$10^{-6}$$.
4. **The statistical machinery**: family-level aggregation, paired bootstrap CIs,
   Holm and BH adjustment.
5. **The frozen selector constants** D1 (threshold 0.0727) and D2
   ($$0.0144 + 0.2592 \cdot \text{cv\_gap}$$), and their behaviour.

## What cannot be reproduced, and why

1. **The Phase 1–7 accuracy figures.** No code, no data, no configurations. They
   remain author-reported.
2. **The historical effect sizes and p-values**, including the corrected audit
   figures (selector vs always-coherent +0.56 pp, 95% CI [−0.59, +1.70], p=.285;
   selector vs RBF −2.03 pp, 95% CI [−7.38, +1.74], p=.552). These are preserved as
   reported findings, marked as not independently reproduced.
3. **The historical baseline comparisons.** The baseline implementations and their
   tuning effort are unavailable.
4. **The D3 selector.** Its threshold and corrected polarity are not recorded
   anywhere in the published material. `src/qcis/selectors.py` therefore implements
   D1 and D2 only. Inventing a threshold would mean fabricating part of the method.
5. **The historical geometry-feature correlations** (rho = +.759, +.772 and so on).
   The exact probe implementation was never published; `features.py` is this
   release's own reproducible definition, and its numbers are not comparable.

## Inconsistencies found in the record, and their status

These are preserved as-is rather than silently corrected, because they are part of
the historical record.

| Item | Finding | Status |
|---|---|---|
| Phase numbering | The record runs Phase 1, 3, 4, 5, 6, 7. There is no Phase 2 write-up. | Preserved; noted in `docs/phase_history.md` |
| Phase 7 selector accuracy | The record contains an unresolved aside ("Selector was 83.88%? The original record reports selector 84.44%...") | Preserved verbatim in `docs/phase_history.md`; the audit figure of 84.44% is used in `RESULTS_SUMMARY.md` |
| `linear_sep` feature | A known defect: it used training accuracy and overfit at high dimension, and was not fixed after the held-out results in that phase | Preserved and reported as a limitation |
| Licence copyright line | Carried an inconsistent attribution string | **Corrected** to "Adarsh K. B." per the required public attribution; the superseded string is not reproduced here |
| `CITATION.cff` type | Declared `type: software` while the repository contained only documentation | **Kept as `software`, and now accurate.** The CFF 1.2.0 schema restricts `type` to `software` or `dataset`, so there is no documentation-only value to switch to and inventing one would make the file invalid. The release now does ship executable code, so `software` is the correct value; the `abstract` states explicitly that this is a reference implementation of the published equations, not the original research code, and not a complete software package |
| Section numbering | Each document carried the dossier's original numbering (e.g. `## 21.`), so standalone documents started at arbitrary numbers | **Corrected**: each standalone document now numbers from 1 |
| `docs/release_dossier.md` | — | **Deliberately not renumbered**: it is the archived provenance record and keeps the original 0–26 numbering, with a header saying so |

## Verification performed for this release

```text
python -m pytest -q                         56 passed
python scripts/run_reproduction.py --all    exit 0, 176 fits, 8 families
python scripts/verify_results.py            PASS, 176 rows within 1e-6
```

## Standing conclusion

This repository is now **accurate and transparent about what it is**: a documented
research project with a working reference implementation of its published
mathematics. It is **not** a reproducibility package for the historical experiments,
and the documentation says so in every place where a reader might otherwise assume
otherwise.
