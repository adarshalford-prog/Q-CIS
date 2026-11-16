# Q-CIS — Research summary

Scope, motivation, research questions, and the consolidated interpretation of the reported evidence.

> **Status note.** This document combines the original research proposal with the later
> experimental findings. The original proposal is a research plan, not evidence that every
> proposed component was implemented. Reported metrics are author-reported summaries; the full
> source code, raw fit-level data, and analysis scripts are not included in this release.

---

## 1. Executive summary

Project QI investigates whether a useful learning architecture can be built around a computational model different from conventional layered neural networks.

The first proposed architecture is **Q-CIS (Quantum Coordinate Intelligence System)**. Its starting idea is to represent information as locations in a multidimensional state space, let multiple candidate interpretations interact through complex-valued amplitudes and phase relationships, and learn through feedback-driven changes to both coordinates and phases.

The initial implementation is intended to run on an ordinary classical computer. It is quantum-inspired, not a physical quantum computer and not a claim that binary hardware has been replaced. The aim is to test whether the mathematical architecture offers measurable benefits over strong classical baselines.

Central research question:

> Can coordinate-based state evolution, combined with phase-sensitive interference and feedback, provide a useful learning and decision mechanism that is meaningfully different from conventional neural-network training?

No performance advantage, general intelligence, or scientific novelty is assumed. Those must be demonstrated.

## 2. Motivation and conceptual distinction

Coordinates and vector spaces are already common in machine learning. Embeddings, metric learning, radial-basis-function models, prototype methods, and learning vector quantisation all use geometric representations. Q-CIS must not claim novelty merely because it uses coordinates.

The proposed combination investigates a system in which:

1. Information is associated with locations in a state space.
2. Candidate interpretations have complex-valued amplitudes and phases.
3. Candidate contributions combine through interference-like mathematics.
4. Feedback changes the geometry and phase relationships.
5. Decisions emerge from the resulting state interactions.

The research task is to define these elements precisely, compare them with existing methods, and determine whether their combination is useful.

## 3. Research objectives

### Primary objective
Specify and test a coordinate-based, phase-sensitive learning architecture that can be simulated on classical hardware.

### Secondary objectives
- Define a mathematical representation for internal states.
- Develop a decision rule based on complex-valued state interactions.
- Develop feedback rules for coordinate and phase updates.
- Compare the system against classical geometric and neural baselines.
- Test whether phase and interference add value beyond coordinates alone.
- Investigate how the architecture might later support structured memory and reasoning.

## 4. Research questions and hypotheses

### RQ1 — Positional learning
Can coordinate-based state evolution learn useful representations without relying on conventional neural-network layers?

**H1:** A coordinate-state system can learn at least some low-dimensional classification tasks using a compact set of internal states.

### RQ2 — Phase and interference
Do phase relationships provide useful information beyond coordinate distance?

**H2:** Trainable phases may improve prediction quality on selected ambiguous or overlapping datasets compared with an otherwise identical phase-free model.

### RQ3 — Combined learning
Does joint coordinate and phase adaptation provide benefits over either mechanism alone?

**H3:** Joint learning may improve one or more of sample efficiency, robustness, or generalisation on selected tasks.

These hypotheses are falsifiable. A negative result is useful research evidence.

## 5. What Q-CIS is not

Q-CIS v0.1 is not:
- A general-purpose AI.
- A demonstrated replacement for neural networks.
- A physical quantum computer.
- A proven faster learning algorithm.
- A model with established long-term memory or reasoning.
- A verified scientific breakthrough.

These are possible future research directions, not current capabilities.

## 6. Success criteria

The first research stage succeeds if it produces:
1. A mathematically unambiguous architecture.
2. A correct and tested implementation.
3. Reproducible experiments.
4. Fair comparisons with relevant classical methods.
5. Ablation results that reveal which components matter.
6. A clear account of limitations and negative results.

A performance claim requires evidence across suitable tasks and repeated experiments. A novelty claim requires careful comparison with prior literature.

---

## 7. What the evidence supports

The reported experiments support cautious statements that:
- A classical coordinate-and-phase classifier was implemented and tested on multiple synthetic dataset families.
- The squared-modulus score has an exact real-valued sine/cosine equivalent in the tested formulation.
- Phase effects are dataset-dependent and can be unstable.
- A nonlinear-minus-linear geometry probe gap showed associations with phase benefit in multiple reported experimental banks.
- A frozen selector classified mechanism choice well on some later evaluation banks.
- The corrected Phase 7 evidence does not establish a reliable practical gain over always-coherent phases.
- Q-CIS did not demonstrate consistent superiority over conventional RBF, SVM, or MLP baselines.

## 8. What the evidence does not support

Do not claim:
- Quantum advantage or physical quantum computation.
- Entanglement or actual quantum superposition.
- A new computational primitive.
- General superiority over RBF, SVM, MLP, or neural networks.
- A reliable practical benefit from the Phase 7 selector over always-coherent phases.
- Equivalence between the selector and RBF based on a nonsignificant comparison.
- General-purpose AI, long-term memory, or reasoning capabilities.
- Independent reproducibility from this release dossier alone.

---

## Further reading

- Mathematical formulation: [MATHEMATICAL_MODEL.md](MATHEMATICAL_MODEL.md)
- Experimental plan and protocol: [METHODOLOGY.md](METHODOLOGY.md)
- Reported results: [RESULTS_SUMMARY.md](RESULTS_SUMMARY.md)
- Limitations and open questions: [LIMITATIONS.md](LIMITATIONS.md)
