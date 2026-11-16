# Q-CIS — a classical coordinate-and-phase classifier

**Public research release, v0.2.0 · 16 November 2026**
**Author:** Adarsh K. B. · **Contact:** adarsh.alford@gmail.com
**Repository:** https://github.com/adarshalford-prog/Q-CIS

---

## Read this first

Q-CIS is a **classical** classifier. "Quantum-inspired" describes the shape of the
mathematics only. There is no quantum computer, no physical quantum state, no
entanglement, and no quantum advantage anywhere in this work, and none is claimed.

This repository is a **partial research release**. It contains:

* research documentation (what was proposed, what was measured, what it means);
* a **reference implementation** of the published equations, written for this release;
* deterministic synthetic dataset generators;
* a test suite covering the mathematical properties and the leakage boundaries;
* a reproduction workflow that runs and verifies against a committed reference output.

It does **not** contain the original experiment code, the raw fit-level data, the
exact configurations, or the analysis scripts behind the **Phase 1–7** figures quoted
in the documentation. Those figures are **author-reported** and are **not**
independently reproducible from this repository. See
[REPOSITORY_AUDIT.md](REPOSITORY_AUDIT.md) for a file-by-file account of what exists
and what is missing.

---

## What Q-CIS is

Information is represented as locations in a multidimensional state space. Each
internal state carries a coordinate vector and a complex-valued amplitude with a
phase. Candidate contributions are **summed as amplitudes before their squared
magnitude is taken**, so phase relationships can reinforce or partially cancel one
another. Learning moves the coordinates, the phases, and the input encoder together.

The class score is a normalised squared-modulus RBF-style expansion. It has an exact
real-valued sine/cosine equivalent, so complex arithmetic is not required to compute
it.

## Mathematical formulation

An input $$x$$ is mapped to a query coordinate $$q = Wx$$. Each state $$i$$ has a
coordinate $$s_i$$, a phase $$\phi_i$$, and a fixed class membership (from training
labels only):

$$
D_i = \lVert q - s_i \rVert^2, \qquad
K_i = \exp\!\left(-\frac{D_i}{2\sigma^2}\right)
$$

$$
r_i = \frac{\sqrt{K_i}}{\sqrt{\sum_j K_j}}
\quad\text{so that}\quad \sum_i r_i^2 = 1, \qquad
a_i = r_i e^{\,i\phi_i}
$$

For class $$c$$ with state index set $$I_c$$:

$$
z_c = \Bigl|\sum_{i \in I_c} a_i\Bigr|^2
      = \Bigl(\sum_{i \in I_c} r_i \cos\phi_i\Bigr)^2
      + \Bigl(\sum_{i \in I_c} r_i \sin\phi_i\Bigr)^2,
\qquad
P(c) = \frac{z_c}{\sum_k z_k}
$$

The right-hand form is exact, and the implementation agrees with the complex form to
about $$10^{-16}$$. Training minimises cross-entropy by gradient descent (Adam) on
$$W$$, $$s_i$$, $$\phi_i$$ and $$\sigma$$. The full derivation, including the
gradients, is in [MATHEMATICAL_MODEL.md](MATHEMATICAL_MODEL.md) and
`src/qcis/model.py`.

### Relationship to existing methods

Every ingredient has substantial prior art, and this release claims **no** new
computational primitive:

* normalised squared-modulus expansions and Gaussian kernels are the machinery of
  **radial basis function** networks;
* moving prototypes toward and away from data is **learning vector quantisation**
  and **prototype learning**;
* a learned linear encoder feeding a geometric classifier is **metric learning**;
* the score is a **rank-one quadratic readout** of the class amplitude vector;
* complex-valued and phase-sensitive networks are an established field.

Whether the *combination* is distinct from these is an open question that needs a
full literature review. [REFERENCES.md](REFERENCES.md) lists verifiable sources for
each ingredient and states plainly what is and is not new.

---

## Install and run

Python 3.9+ and NumPy are the only runtime requirements.

```bash
git clone https://github.com/adarshalford-prog/Q-CIS.git
cd Q-CIS
python -m pip install -r requirements.txt
```

Use the package directly:

```python
import sys; sys.path.insert(0, "src")
from qcis import QCISClassifier

clf = QCISClassifier(mechanism="trained_phase", n_states_per_class=8, dim=4)
clf.fit(X_train, y_train, epochs=200, lr=0.05, seed=0)
print(clf.score(X_test, y_test))
```

Available mechanisms, matching the original ablation plan:

| `mechanism` | Ablation | What it does |
|---|---|---|
| `coords_only` | A | $$z_c = \sum_{i \in I_c} r_i^2$$ — no interference at all |
| `incoherent` | D | phases pinned to zero, $$z_c = (\sum_{i \in I_c} r_i)^2$$ |
| `fixed_phase` | B | phases drawn once at random, then held fixed |
| `trained_phase` | C / E / F | phases learned with the coordinates |

## Reproduce the results

One command, from a clean environment:

```bash
python scripts/run_reproduction.py --all
python scripts/verify_results.py
```

The first generates the documented synthetic families from fixed seeds, runs every
mechanism across all families and seeds, runs two classical baselines, and writes the
family-level statistical audit to `results/raw/` and `results/summaries/`. The second
compares that output against the committed reference in `results/reference/` and exits
non-zero on any discrepancy.

Full instructions, tolerances and troubleshooting: [REPRODUCIBILITY.md](REPRODUCIBILITY.md).

### What is independently reproducible, and what is not

| | Status |
|---|---|
| The published mathematics (normalisation, complex/real equivalence, phase invariance, score properties) | **Reproducible** — covered by tests |
| The reference implementation on the documented synthetic families | **Reproducible** — one command, verified against a committed reference |
| The family-level statistics machinery (bootstrap CIs, Holm correction, family as the unit) | **Reproducible** — covered by tests |
| The frozen selector constants D1 and D2 | **Reproducible** — the constants are published and tested |
| The **Phase 1–7 accuracy figures**, effect sizes and p-values | **Author-reported only** — code, raw data and configurations were never published |
| The historical baseline comparisons ("behind RBF by 3.33 points" and similar) | **Author-reported only** — the original baselines are unavailable |
| The historical D3 selector | **Not reproducible** — its threshold and corrected polarity are not recorded |

Nothing in this repository should be read as an independent reproduction of the
historical figures.

---

## Known limitations

The short version; the full list is in [LIMITATIONS.md](LIMITATIONS.md).

1. **No demonstrated advantage.** Q-CIS was reported behind RBF, SVM and MLP
   baselines, and the corrected Phase 7 audit found no statistically established
   benefit from trained phases over always-coherent phases.
2. **The real-valued form is sufficient.** Complex arithmetic is not needed to
   compute the score, which undercuts the motivation for the complex framing.
3. **Phase instability.** Refitting phases with frozen coordinates caused large
   accuracy drops in the historical record.
4. **Dataset dependence.** Behaviour varied sharply across geometries; concentric
   rings and high-dimensional shells exposed clear weaknesses.
5. **Small numbers of independent units.** The Phase 7 bank had 18 families, so
   confidence intervals are wide.
6. **Selector utility is unproven.** Predicting which mechanism wins on a family
   does not guarantee a useful accuracy gain.
7. **Novelty is unresolved.** A systematic literature review is required before any
   novelty claim.

### A note on this release's own results

Running the reference implementation here produces small, honest numbers: on the
eight families in `results/summaries/summary.md`, trained phases are **not**
distinguishable from fixed, incoherent or coordinate-only phases, and the model does
not beat a Gaussian-kernel ridge baseline. Those are results of *this* reference
implementation on *newly generated* data. They are consistent in direction with the
historical conclusion, but they are not a reproduction of it, and they must not be
cited as one.

---

## Repository layout

```text
Q-CIS/
├── README.md                  this file
├── LICENSE                    MIT
├── CITATION.cff               citation metadata
├── REPOSITORY_AUDIT.md        what exists, what is missing, what is reproducible
├── REPRODUCIBILITY.md         step-by-step instructions for an outside researcher
├── REFERENCES.md              verified sources for the prior art
├── pyproject.toml             package metadata
├── requirements.txt           pinned requirements
├── RESEARCH_SUMMARY.md        motivation, questions, consolidated interpretation
├── MATHEMATICAL_MODEL.md      the equations and their interpretation boundary
├── METHODOLOGY.md             protocol, prototype specification, roadmap
├── RESULTS_SUMMARY.md         reported results, Phase 1-7 and the audit
├── LIMITATIONS.md             risks, limitations, open questions
├── src/qcis/                  reference implementation
├── datasets/generation/       deterministic synthetic generators
├── experiments/               benchmark runner and configs
├── analysis/                  family-level statistical audit
├── scripts/                   one-command reproduction and verification
├── tests/                     mathematical, gradient, leakage and command tests
├── results/                   raw, summaries, committed reference output
├── .github/workflows/         CI (smoke tests only, labelled as such)
└── docs/                      original proposal, phase history, audit, full dossier
```

## Cite this work

See [CITATION.cff](CITATION.cff). This is a **research project and documentation
release with a reference implementation**; it is not a complete software package and
should not be cited as one.

## Contact

Questions about the methodology, or requests for additional experimental detail:
**adarsh.alford@gmail.com**

## Licence

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Adarsh K. B.

The licence grants use of this material; it does not establish scientific validity,
and it does not grant rights over third-party components. This release contains no
third-party code or data.
