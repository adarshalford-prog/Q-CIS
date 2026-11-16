# Reproducibility guide

Instructions for a researcher who has never spoken to the author: clone, install,
run, and check the result against a committed reference.

This guide reproduces **this release's reference implementation on newly generated
synthetic data**. It does **not** reproduce the historical Phase 1–7 figures, which
cannot be reproduced from this repository at all. See
[REPOSITORY_AUDIT.md](REPOSITORY_AUDIT.md) for why.

---

## 1. Supported systems and Python version

| | |
|---|---|
| Operating systems | Linux, macOS, Windows (anything with a working CPython and BLAS) |
| Python | **3.9 or newer** (CI runs 3.9 and 3.12) |
| Runtime dependencies | NumPy only |
| Test dependency | pytest |
| GPU | not required, not used |
| Network | not required at run time — no dataset is downloaded |

Verified on: Python 3.12.13, NumPy 2.5.4, Linux x86_64. CI additionally covers
Python 3.9.

## 2. Create an environment

```bash
git clone https://github.com/adarshalford-prog/Q-CIS.git
cd Q-CIS
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

This installs NumPy and pytest. Nothing else is needed.

The package can optionally be installed into the environment, though the scripts set
`sys.path` themselves and do not require it:

```bash
python -m pip install -e .
```

## 4. Dataset preparation

There is nothing to download. Every dataset is generated in-process from a seed by
`datasets/generation/synthetic.py`. The eight documented families and their exact
parameters are listed in [datasets/README.md](datasets/README.md).

To inspect a family without running anything else:

```bash
PYTHONPATH=src:. python -c "
from datasets.generation.synthetic import make, stratified_split
X, y = make('spirals', seed=20261116)
tr, te = stratified_split(y, seed=20261116)
print(X.shape, y.shape, len(tr), len(te))
"
```

## 5. Run a single experiment

Fit one model on one family:

```bash
PYTHONPATH=src:. python -c "
import sys
from datasets.generation.synthetic import make, stratified_split
from qcis import QCISClassifier

X, y = make('spirals', seed=20261116)
tr, te = stratified_split(y, seed=20261116)

for mech in ('coords_only', 'incoherent', 'fixed_phase', 'trained_phase'):
    clf = QCISClassifier(mechanism=mech, n_states_per_class=8, dim=4)
    clf.fit(X[tr], y[tr], epochs=200, lr=0.05, seed=0)
    print(f'{mech:15s} train {clf.score(X[tr], y[tr]):.4f}  test {clf.score(X[te], y[te]):.4f}')
"
```

## 6. Run the full available suite

```bash
python scripts/run_reproduction.py --all
```

This runs, in order:

1. `experiments/run_benchmark.py` — 8 families × 4 mechanisms × 5 seeds, plus two
   baselines per family, writing `results/raw/fits.csv` and
   `results/raw/fits_env.json`;
2. `analysis/audit.py` — family-level statistics, writing
   `results/summaries/{audit.json,summary.csv,summary.md}`.

Expected runtime: about **90 seconds** on 2 CPU cores for the default configuration.
It exits non-zero if any stage fails.

To start from scratch, add `--force` (the benchmark refuses to overwrite existing
output unless told to, so historical records are never clobbered by accident).

## 7. Run the tests

```bash
PYTHONPATH=src:. python -m pytest -q
```

Expected: **56 passed**. The suite covers:

| File | What it proves |
|---|---|
| `tests/test_scoring.py` | normalisation $$\sum_i r_i^2 = 1$$, exact complex/real equivalence, non-negativity and finiteness, numerical stability at extreme distances, 2π and global-phase invariance |
| `tests/test_gradients.py` | every analytic gradient against finite differences, for all four mechanisms, including the cross terms through the shared normaliser |
| `tests/test_determinism.py` | identical seeds give bit-identical parameters and predictions |
| `tests/test_no_leakage.py` | splits are disjoint and stratified; features are unchanged when the test half is poisoned; test labels cannot change a fitted model |
| `tests/test_selectors.py` | the frozen D1 and D2 constants and switch points |
| `tests/test_stats.py` | bootstrap CIs, Holm and BH monotonicity, McNemar |
| `tests/test_commands.py` | the documented commands run and return meaningful exit codes |

## 8. Reproduce the tables

`results/summaries/summary.md` is generated, not hand-written. Running step 6
regenerates it. It contains:

* family-level mean test accuracy per mechanism;
* paired family-level contrasts with bootstrap confidence intervals, raw p-values and
  Holm-adjusted p-values;
* the geometry-gap-versus-phase-benefit correlation (descriptive only);
* frozen-selector behaviour.

There are no figures to reproduce; this release ships no plots.

## 9. Compare with the reference output

```bash
python scripts/verify_results.py
```

Expected output:

```text
compared 176 rows against reference_fits.csv (tolerance 1e-06)
PASS: reproduction matches the reference output within tolerance
```

### Documented tolerances

| Column | Tolerance |
|---|---|
| `train_accuracy`, `test_accuracy` | $$10^{-6}$$ absolute |
| `final_loss` | $$10^{-6}$$ absolute |
| `cv_linear`, `cv_nonlinear`, `cv_gap`, `cv_1nn`, `fisher_ratio` | $$10^{-6}$$ absolute |
| `n_states`, `n_params`, `n_train`, `n_test` | exact |
| `fit_seconds` | **excluded** — wall-clock timing |

The implementation is deterministic given a seed, so exact agreement is the expected
result. The tolerance exists only because different BLAS builds may reassociate
floating-point sums.

### What the reference file is

`results/reference/reference_fits.csv` is the **output of this release's reference
implementation**, committed so you can tell a correct run from a broken one. It
contains no historical numbers.

## 10. Troubleshooting

**`ModuleNotFoundError: No module named 'qcis'`**
The scripts add `src/` to `sys.path` themselves, so run them from the repository
root. For your own code, set `PYTHONPATH=src:.` or `pip install -e .`.

**`ModuleNotFoundError: No module named 'datasets'`**
Same cause. Include the repository root on the path: `PYTHONPATH=src:.`.

**`refusing to overwrite results/raw/fits.csv`**
Intentional. Pass `--force` if you mean to replace it.

**`verify_results.py` reports small discrepancies around 1e-9**
Harmless; that is BLAS reassociation. If you see differences above 1e-6, check that
you did not modify `experiments/configs/default.json`, and confirm your NumPy version.

**Results differ substantially between runs**
They should not. Check that `base_seed` in the config is unchanged and that you are
not passing a different `--seed` to `analysis/audit.py` — the bootstrap resampling
depends on it, though the underlying accuracies do not.

**Tests are slow**
`tests/test_commands.py` invokes the real command-line entry points on a tiny
configuration, so it is the slowest file. If you want a quick run, point pytest at
the other test files only and leave `tests/test_commands.py` out.

**Windows path issues**
The scripts build paths with `os.path.join` and run from the repository root, so they
work on Windows. Use the PowerShell activation shown in step 2.

---

## What cannot be reproduced, and what to do instead

| Cannot be reproduced | Why | What to do |
|---|---|---|
| Phase 1–7 accuracies, effect sizes, p-values | Original code, raw data and configs were never published | Read them as author-reported in [RESULTS_SUMMARY.md](RESULTS_SUMMARY.md); do not cite as reproduced |
| Historical baseline comparisons | The original baseline implementations are unavailable | Use the baselines in `src/qcis/baselines.py` for this release's code only |
| Historical geometry-feature correlations | The original probe implementation was never published | `src/qcis/features.py` is this release's own definition; its numbers are not comparable |
| The D3 selector | Its threshold and corrected polarity are not recorded | Not implemented, by design |

If you need the historical detail that is missing here, the honest route is to ask
the author: **adarsh.alford@gmail.com**. Nothing in this repository requires access
to the author's private machine, private storage, or any unpublished file.
