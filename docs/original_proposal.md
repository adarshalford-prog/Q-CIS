# Q-CIS — Original research proposal (Part I)

The original proposal as recorded, reproduced in full. It is a research plan, not evidence that
every proposed component was implemented.

> Source document: **Project_QI_QCIS_Research_Proposal_v0.1.md**

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

## 4. Proposed architecture

The initial proposed pipeline is:

**Input → Coordinate encoding → Candidate-state retrieval → Complex amplitude assignment → Interference-based decision → Feedback → Coordinate and phase updates → Persistent state memory**

### 4.1 Coordinate state space

Let the system contain internal states:

$$
S=\{s_1,s_2,\ldots,s_N\}
$$

Each state has a coordinate vector:

$$
s_i=(x_{i1},x_{i2},\ldots,x_{id})\in\mathbb{R}^d
$$

Where:
- $N$ is the number of internal states.
- $d$ is the coordinate-space dimensionality.
- $x_{ij}$ is coordinate $j$ of state $i$.

An input observation is encoded as a query vector:

$$
q(x)\in\mathbb{R}^d
$$

A basic geometric distance is:

$$
D(q,s_i)=\|q-s_i\|_2^2
$$

The initial prototype may use a fixed input encoder or simple hand-designed features. A learned encoder should be treated as a separate experimental component because it could introduce conventional neural-network learning and obscure what Q-CIS itself contributes.

### 4.2 Complex-valued amplitudes and phases

Associate each candidate state with a complex amplitude:

$$
a_i=r_i e^{\mathrm{i}\phi_i}
$$

Where:
- $r_i\geq 0$ is amplitude magnitude.
- $\phi_i$ is phase.
- $\mathrm{i}^2=-1$.

For a distance-based starting point:

$$
w_i=\exp\left(-\frac{D(q,s_i)}{2\sigma^2}\right)
$$

$$
r_i=\frac{\sqrt{w_i}}{\sqrt{\sum_k w_k}}
$$

This normalizes the magnitudes so that:

$$
\sum_i r_i^2=1
$$

The phase $\phi_i$ is an additional trainable or state-dependent quantity. Its initialization and update rule must be specified experimentally.

This construction is a quantum-inspired mathematical representation. It does not by itself create a physical quantum state or quantum computational advantage.

### 4.3 Interference-based decision

Suppose each internal state contributes to a candidate class or answer $c$. Let $I_c$ be the indices of states associated with that candidate.

Combine their amplitudes:

$$
A_c=\sum_{i\in I_c}a_i
$$

Define a score:

$$
z_c=|A_c|^2
$$

Convert scores into normalized decision probabilities:

$$
P(c)=\frac{z_c}{\sum_k z_k}
$$

Because amplitudes are added before their squared magnitudes are calculated, phase relationships can reinforce or partially cancel contributions. This is the proposed interference mechanism.

Important implementation issue: if states are grouped by class, the grouping must be learned or defined without leaking test labels. The system also needs a principled way to handle multiple, overlapping, or context-dependent relationships.

### 4.4 Coordinate-based learning

A general optimization form for a contributing state is:

$$
s_i^{(t+1)}=s_i^{(t)}-\eta_s\nabla_{s_i}L
$$

Where:
- $t$ is the update step.
- $L$ is a defined prediction loss.
- $\eta_s$ is the coordinate learning rate.

An interpretable prototype may also test attraction and repulsion rules:
- Pull a state toward observations it should represent.
- Push it away from observations it repeatedly confuses.
- Preserve useful relationships between related states.
- Limit update size to avoid unstable movement.

This resembles existing prototype learning, metric learning, and learning vector quantisation. The experimental contribution must therefore lie in the complete learning rule and its measured behaviour, not in attraction or repulsion alone.

### 4.5 Phase-based learning

The phase can be updated using a loss gradient:

$$
\phi_i^{(t+1)}=\phi_i^{(t)}-\eta_\phi\frac{\partial L}{\partial\phi_i}
$$

Where $\eta_\phi$ is the phase learning rate.

The phase update should be wrapped modulo $2\pi$, and numerical stability must be checked.

The hypothesis is that phase updates can improve the way competing candidate states combine. This is not guaranteed. The system must be tested against an otherwise identical model with phases fixed, randomized, or removed.

### 4.6 Combined learning cycle

The proposed training cycle is:

1. Receive an input observation.
2. Encode it as a coordinate query.
3. Retrieve relevant internal states.
4. Calculate state magnitudes and phases.
5. Combine candidate amplitudes.
6. Produce a prediction and confidence distribution.
7. Receive a trusted target or feedback signal.
8. Calculate a loss.
9. Update coordinates and phases.
10. Save the revised state and relevant relationship information.

Correct predictions should not automatically be reinforced without qualification. Updates should depend on loss, confidence, evidence quality, and contradictory examples. Otherwise, the system may become overconfident or reinforce incorrect labels.

## 5. Existing equivalents and related research

The individual ingredients have substantial precedents. Relevant overlap includes:

| Related field or method | Relevant overlap |
|---|---|
| Embedding models | Represent information as vectors in a space |
| Metric learning | Learn distances and relationships between examples |
| Learning Vector Quantisation | Move prototypes to improve classification |
| Radial Basis Function models | Use distance-based responses around centres |
| Prototype networks | Represent classes or concepts with representative states |
| Complex-valued neural networks | Use complex numbers and phase-sensitive operations |
| Quantum-inspired machine learning | Use mathematical structures inspired by quantum theory on classical hardware |
| Quantum cognition | Use quantum probability formalisms to model certain cognitive phenomena |
| Quantum machine learning | Investigate learning algorithms using quantum computation |

### Novelty position

At proposal stage, Q-CIS is a **research hypothesis**, not an established original discovery.

A systematic literature review is required before making any novelty claim. It should search for prior work combining:
- Coordinate or prototype state evolution.
- Complex amplitudes and phase.
- Interference-based classification or decision.
- Feedback-driven updates to both positions and phases.
- Persistent state memory and compositional relationships.

The exact equations, training rules, data structures, and experimental results must be compared with the closest prior work.

## 6. Research questions and hypotheses

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

## 7. Experimental plan in the original proposal

### 7.1 Initial datasets
1. XOR — tests nonlinear separability.
2. Concentric circles — tests curved decision boundaries.
3. Overlapping clusters — tests ambiguity and competing interpretations.

Use fixed random seeds and documented train, validation, and test splits. Do not tune on the test set.

### 7.2 Comparison models
1. Nearest-centroid classifier.
2. Radial Basis Function classifier.
3. Learning Vector Quantisation or another prototype-learning baseline.
4. A small multilayer perceptron.
5. A relevant complex-valued or quantum-inspired baseline, where a suitable reproducible implementation is available.

Baselines should receive comparable tuning effort and appropriate capacity. Report parameter counts or state counts and computational costs.

### 7.3 Ablation studies

| Version | Components |
|---|---|
| A | Coordinates only |
| B | Coordinates + fixed phases |
| C | Coordinates + trainable phases |
| D | Coordinates + interference, without phase learning |
| E | Coordinates + feedback-based phase learning |
| F | Full Q-CIS: coordinate and phase learning |

These tests identify whether each proposed mechanism contributes anything measurable.

### 7.4 Metrics
Record:
- Accuracy and macro-F1 where appropriate.
- Cross-entropy or another suitable loss.
- Calibration and confidence quality.
- Learning curves and data efficiency.
- Robustness under controlled input noise.
- Training and inference time.
- Memory use.
- Number of internal states and trainable parameters.
- Run-to-run variability across multiple seeds.

Do not select only the metric on which Q-CIS performs best. Report all predeclared metrics.

## 8. Main technical risks

### 8.1 No demonstrated advantage
Coordinates and complex amplitudes may simply reproduce behaviour that classical models already achieve more efficiently. Response: use strong baselines and ablations; treat equal or worse performance as a valid result.

### 8.2 State-space scaling
The number of internal states and the cost of comparing an input with them may grow substantially. Response: begin with small state collections, measure scaling, and investigate sparse retrieval only after the basic model is validated.

### 8.3 Phase instability
Phase updates may oscillate, become uninformative, or make optimization difficult. Response: use bounded learning rates, phase wrapping, gradient checks, and controlled fixed-phase comparisons.

### 8.4 Ambiguous state relationships
A state may be relevant to several concepts or classes. Simple class grouping may be too restrictive. Response: later investigate explicit relationship graphs, context-dependent associations, or compositional state structures. Do not add these before the initial model is understood.

### 8.5 Overfitting and feedback errors
A system that moves states toward every observed label may memorize noise or reinforce bad feedback. Response: use validation, regularisation, confidence-aware updates, and noisy-label experiments.

### 8.6 Quantum terminology overstated
A complex-valued classical simulation is not a quantum computer. Quantum-inspired equations do not establish physical superposition, entanglement, or quantum speedup. Describe the implementation accurately as a classical quantum-inspired model unless a genuine quantum circuit or physical quantum system is used.

## 9. Original first-prototype specification: Q-CIS v0.1

| Component | Initial target |
|---|---|
| Execution | CPU |
| Implementation | Python and NumPy |
| Coordinate dimensions | 2–16 |
| Internal states | 100–1,000 |
| Amplitudes | Complex-valued |
| Phases | Trainable |
| Input | Small numerical feature vectors |
| Task | Synthetic classification |
| Learning | Coordinate and phase updates |
| Visualisation | 2D state-space plots and learning curves |

These ranges are starting experiment settings, not optimal values.

### Suggested original software structure

```text
project-qi/
├── README.md
├── docs/
│   ├── research-proposal.md
│   ├── mathematical-model.md
│   └── experiment-protocol.md
├── qcis/
│   ├── state_space.py
│   ├── amplitudes.py
│   ├── interference.py
│   ├── learning.py
│   ├── memory.py
│   └── model.py
├── experiments/
│   ├── xor.py
│   ├── circles.py
│   ├── overlapping_clusters.py
│   └── ablations.py
├── baselines/
├── tests/
└── results/
```

## 10. Original development roadmap

### Stage 1 — Formal specification
Define input encoder, state initialization, candidate retrieval, amplitude and phase calculations, decision rule, coordinate and phase losses; check normalization and numerical stability.

**Deliverable:** Complete mathematical specification.

### Stage 2 — Minimal simulator
Implement coordinate space, complex amplitudes, interference scoring, coordinate updates, phase updates, and unit tests.

**Deliverable:** Working CPU-based Q-CIS classifier.

### Stage 3 — Baseline evaluation
Run synthetic datasets, compare classical models, run ablations, repeat across seeds, record runtime and memory.

**Deliverable:** Reproducible results and honest performance assessment.

### Stage 4 — Structured memory (future proposal)
If initial model justifies further work, investigate persistent state identities, relationships between states, multiple contexts for the same state, updating/retrieving old information, and conflict resolution.

**Deliverable:** State-based memory experiment.

### Stage 5 — Reasoning experiments (future proposal)
Only after memory and representation are validated, investigate combining multiple observations, resolving competing interpretations, multi-step inference, generalisation to unfamiliar combinations, and language or multimodal input.

**Deliverable:** Separate reasoning prototype with appropriate baselines.

## 11. What Q-CIS is not

Q-CIS v0.1 is not:
- A general-purpose AI.
- A demonstrated replacement for neural networks.
- A physical quantum computer.
- A proven faster learning algorithm.
- A model with established long-term memory or reasoning.
- A verified scientific breakthrough.

These are possible future research directions, not current capabilities.

## 12. Success criteria

The first research stage succeeds if it produces:
1. A mathematically unambiguous architecture.
2. A correct and tested implementation.
3. Reproducible experiments.
4. Fair comparisons with relevant classical methods.
5. Ablation results that reveal which components matter.
6. A clear account of limitations and negative results.

A performance claim requires evidence across suitable tasks and repeated experiments. A novelty claim requires careful comparison with prior literature.

---
