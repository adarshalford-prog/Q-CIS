# Results

Three subdirectories, with a strict separation between what is generated and what is
archived.

## `raw/`

Written by `scripts/run_reproduction.py`. One row per fit, plus an `_env.json`
recording the Python and NumPy versions, platform, configuration and elapsed time.
Nothing in this directory is committed except by explicit choice; it is regenerated
on every run.

## `summaries/`

Written by `analysis/audit.py`:

* `summary.md` — human-readable family-level means, paired contrasts with bootstrap
  confidence intervals and Holm-adjusted p-values, geometry-gap correlation, and
  frozen-selector behaviour;
* `summary.csv` — the family-level means as a table;
* `audit.json` — the same content, machine-readable.

## `reference/`

The committed reference output that `scripts/verify_results.py` checks against.

**`reference_fits.csv` is the output of the reference implementation in `src/qcis`,
not a historical record.** It contains no Phase 1–7 numbers. Its only purpose is to
let an outside researcher confirm that their run of `scripts/run_reproduction.py`
matches a known-good run of the same code.

Tolerance policy: accuracies and cross-validated features to $$10^{-6}$$ absolute,
integer counts exact, wall-clock timings excluded.

## Where the historical numbers live

The Phase 1–7 figures are **not** in this directory. They are quoted, as
author-reported values, in [../RESULTS_SUMMARY.md](../RESULTS_SUMMARY.md) and
[../docs/phase_history.md](../docs/phase_history.md). No raw data for them was ever
published, so they cannot be recomputed from anything here.
