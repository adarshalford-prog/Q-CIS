# Datasets

Every dataset used in this repository is **generated synthetically** by
`generation/synthetic.py`. Nothing is downloaded, nothing is redistributed, and no
third-party data licence applies.

This is deliberate. The original Phase 1–7 runs also used synthetic families, but the
generators themselves were never published, so the exact data behind the historical
figures cannot be reconstructed. The generators here are written for this release to
produce families of the **same shape** — XOR, concentric circles, overlapping
clusters, spirals, moons, rings, high-dimensional shells — not the same samples.

## Determinism

Every generator is a pure function of its seed and parameters. The same seed always
produces bit-identical arrays, which is asserted in `tests/test_determinism.py`.

## Documented families

These are the exact configurations used by `scripts/run_reproduction.py`, from
`FAMILIES` in `generation/synthetic.py`:

| Family | n | d | noise | What it tests |
|---|---|---|---|---|
| `xor` | 400 | 2 | 0.15 | nonlinear separability |
| `circles` | 400 | 2 | 0.10 | curved decision boundaries |
| `overlapping_clusters` | 400 | 2 | 0.85 | ambiguity, irreducible error |
| `spirals` | 400 | 2 | 0.08 | the task where phase effects were reported to matter |
| `moons` | 400 | 2 | 0.10 | interleaving half circles |
| `rings` | 400 | 2 | 0.05 | alternating concentric rings (a known weakness) |
| `shells` | 400 | 20 | 0.05 | high-dimensional shells (a known weakness) |
| `blobs` | 400 | 4 | 0.60 | a well-separated three-class control |

Splits are stratified and drawn from the base seed alone; see `stratified_split()`.

## Adding a family

Add a function to `generation/synthetic.py`, register it in `GENERATORS`, add its
defaults to `FAMILIES`, and add it to `families` in
`experiments/configs/default.json`. Then regenerate the reference output:

```bash
python scripts/run_reproduction.py --all --force
cp results/raw/fits.csv results/reference/reference_fits.csv
```

## Licence

The generators in this directory are part of this repository and are covered by the
repository's MIT licence.
