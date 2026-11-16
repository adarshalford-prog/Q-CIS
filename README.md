# Q-CIS — Quantum Coordinate Intelligence System

**A classical, quantum-inspired learning architecture — partial public research release.**

**Author:** Adarsh K. B. · **Contact:** adarsh.alford@gmail.com
**Version:** 0.1.0 · **Release date:** 16 November 2026
**Repository:** https://github.com/adarshalford-prog/Q-CIS

---

## Read this first

This repository is a **partial public research release**. It contains research documentation,
reported experimental findings, and the project's own account of what the results do and do not
support. It does **not** contain the implementation source code, the raw fit-level data, the exact
configurations, or the analysis scripts. The metrics reported here are **author-reported
summaries** and cannot be independently reproduced from this repository alone.

Q-CIS is a **classical** algorithm. "Quantum-inspired" describes a mathematical analogy only.
No quantum computer, physical quantum state, entanglement, or quantum advantage is claimed.

A full literature review is required before any novelty claim is made. The individual ingredients
of the method have substantial prior art (see [MATHEMATICAL_MODEL.md](MATHEMATICAL_MODEL.md#relationship-to-existing-methods)).

---

## What is here

| Document | Contents |
|---|---|
| [RESEARCH_SUMMARY.md](RESEARCH_SUMMARY.md) | Motivation, research questions and hypotheses, scope, and the consolidated interpretation of the evidence |
| [MATHEMATICAL_MODEL.md](MATHEMATICAL_MODEL.md) | Proposed architecture, state/amplitude/phase/interference equations, the real-valued equivalent, and the interpretation boundary |
| [METHODOLOGY.md](METHODOLOGY.md) | Experimental plan, datasets, baselines, ablations, metrics, prototype specification, and development roadmap |
| [RESULTS_SUMMARY.md](RESULTS_SUMMARY.md) | Headline reported results across Phases 1–7 and the corrected Phase 7 statistical audit |
| [LIMITATIONS.md](LIMITATIONS.md) | Technical risks, known limitations, and open questions |
| [docs/original_proposal.md](docs/original_proposal.md) | The original research proposal (Part I) in full |
| [docs/phase_history.md](docs/phase_history.md) | The reported experimental history, Phases 1–7 |
| [docs/statistical_audit_summary.md](docs/statistical_audit_summary.md) | The Phase 7 statistical audit and corrected inference |
| [docs/release_dossier.md](docs/release_dossier.md) | The complete public release dossier as a single document |

---

## Summary of the method

Information is represented as locations in a multidimensional state space. Each internal state
carries a coordinate vector and a complex-valued amplitude with a phase. Candidate contributions
are summed as amplitudes before their squared magnitude is taken, so phase relationships can
reinforce or partially cancel one another. Learning moves both coordinates and phases.

The class score is a normalized squared-modulus RBF-style expansion, which has an exact
real-valued sine/cosine equivalent — complex arithmetic is not required to compute it.

---

## What the evidence supports

- A classical coordinate-and-phase classifier was implemented and tested on multiple synthetic
  dataset families.
- The squared-modulus score has an exact real-valued sine/cosine equivalent in the tested
  formulation (agreement to approximately $2.2\times10^{-16}$).
- Phase effects are dataset-dependent and can be unstable.
- A nonlinear-minus-linear geometry probe gap showed associations with phase benefit across
  multiple reported experimental banks.
- A frozen selector classified mechanism choice well on some later evaluation banks.

## What the evidence does not support

- No quantum advantage, physical quantum computation, entanglement, or quantum superposition.
- No new computational primitive.
- No general superiority over RBF, SVM, MLP, or neural networks. Q-CIS was **behind** RBF and SVM
  in the reported aggregate comparisons.
- No reliable practical benefit from the Phase 7 selector over always-coherent phases; after the
  statistical audit corrected the inferential unit to the dataset family, that contrast was not
  statistically established.
- No general-purpose AI, long-term memory, or reasoning capability.
- No independent reproducibility from this repository alone.

See [LIMITATIONS.md](LIMITATIONS.md) for the full list.

---

## Contact

This repository contains a partial public research release and selected reported findings. The
complete experimental archive and some supporting materials are not included. If you would like
additional experimental details, supporting results, or have questions about the methodology,
please contact **adarsh.alford@gmail.com**.

## Licence

MIT License — see [LICENSE](LICENSE). Copyright (c) 2026 Adarsh K. B.

The licence does not establish scientific validity or authorship of third-party components.
