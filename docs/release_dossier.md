# Q-CIS — Complete public release dossier (archived source document)

> **Archival note.** This file is the release dossier exactly as prepared, kept as the
> provenance record for the repository. It retains the **original dossier section
> numbering (0-26)**, which deliberately does not match the numbering of the curated
> documents at the repository root and in `docs/`. Those curated documents are each
> numbered independently from section 1. Nothing here has been renumbered or
> rewritten, so that the source of every claim stays traceable.

---

## 0. Release status and accuracy statement

This document combines (a) the original Q-CIS research proposal and (b) the later experimental findings and Phase 7 statistical audit recorded by the project author.

The original proposal is a research plan, not evidence that every proposed component was implemented. The later phases describe the experimental work reported by the author. The full source code, raw fit-level data, exact configurations, and analysis scripts are not included in this document. Therefore, the reported metrics are **author-reported summaries** and cannot be independently reproduced from this document alone.

Q-CIS is a **classical** algorithm. “Quantum-inspired” describes the mathematical analogy. No quantum computer, physical quantum state, entanglement, or quantum advantage is claimed.

The initial public release should be transparent about its partial status. Do not label this dossier as a complete reproducibility package or claim the code is included unless the actual implementation is separately reviewed and published.

---

# Part I — Original research proposal

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

# Part II — Experimental formulation used in later Q-CIS work

## 13. Later classifier formulation

The later experimental classifier uses a learned input coordinate representation $q(x)\in\mathbb{R}^d$ and learned state coordinates $s_i\in\mathbb{R}^d$.

Squared distance:

$$
D_i=\|q(x)-s_i\|^2
$$

Gaussian similarity:

$$
K_i=\exp\left(-\frac{D_i}{2\sigma^2}\right)
$$

Normalized amplitude magnitude:

$$
r_i=\frac{\sqrt{K_i}}{\sqrt{\sum_j K_j}}
$$

Phase-bearing amplitude:

$$
a_i=r_i e^{i\phi_i}
$$

For class $c$, with state index set $I_c$, the class score is:

$$
z_c=\left|\sum_{i\in I_c}r_i e^{i\phi_i}\right|^2
$$

Expanding the squared modulus:

$$
z_c=\sum_{i\in I_c}r_i^2+
2\sum_{\substack{i<j\\i,j\in I_c}}r_ir_j\cos(\phi_i-\phi_j)
$$

The first term is the sum of individual magnitude contributions. The second term contains pairwise phase-dependent interactions.

### 13.1 Real-valued equivalent

The same class score can be computed without complex arithmetic:

$$
z_c=
\left(\sum_{i\in I_c}r_i\cos\phi_i\right)^2+
\left(\sum_{i\in I_c}r_i\sin\phi_i\right)^2
$$

The reported real-valued and complex implementations matched to approximately $2.2\times10^{-16}$ in the tested implementation. The real-valued version was reported to be about 3% faster in the Phase 4 comparison. Complex arithmetic is not essential to compute this score.

### 13.2 Interpretation boundary

This is a classical normalized squared-modulus RBF-style expansion / rank-one quadratic readout. The use of complex notation does not establish physical quantum superposition, entanglement, or quantum advantage. The method's ingredients overlap with established areas including embeddings, metric learning, RBF methods, prototype learning, and complex-valued models.

No claim of a new computational primitive is made.

---

# Part III — Reported experimental history (Phases 1–7)

**Important:** The following values and descriptions are transcribed from the project's recorded research history. They are not independently recalculated in this document because the raw data and executable analysis archive are not attached here.

## 14. Phase 1 — Initial prototype, ablations, and corrections

The initial prototype evaluated synthetic datasets including XOR, circles, overlapping clusters, and spirals. It compared coordinate-only and phase-based variants and conventional baselines.

Implementation/reporting corrections included:
- Analytic gradient was 8× too large because batch-mean division was missing; after correction, finite-difference error was approximately $1.6\times10^{-9}$.
- Coordinate-gradient broadcasting error was corrected.
- GLVQ loss sign was inverted and corrected.
- MLP underfit on circles due to early stopping; this was corrected.
- RBF k-means requested too many centres; corrected.
- Dimension padding by orthonormal columns was a no-op for a distance-only model; replaced by polynomial feature lift.
- Reporting issues were corrected, including dimension-sweep key collision, McNemar direction labels, drift statistic field, and Word equation parser.

Study 1 used 5 seeds × 4 datasets. Reported Q-CIS coordinate-only scores:
- XOR: 94.8
- Circles: 99.0
- Overlap: 69.6
- Spirals: 82.5

Phase variants helped some spiral experiments, but trained-phase improvement over fixed random phase was small.

Study 2 contained 1,120 fits. Fixed versus trained phase was reported as +0.14 percentage points, CI approximately −0.01 to +0.28, p=.074. 88/120 paired units were identical. The initial five-seed comparison had p=.374.

**Interpretation:** Phase encoding may help on selected tasks, but a general benefit from training phases was not established.

## 15. Phase 3 — Independent reproduction and falsification

Reported findings:
- Independent reproduction: 36/36 model-dataset cells bit-for-bit identical.
- Q-CIS was behind RBF by 3.33 points (BH-adjusted p=.010) and behind SVM by 2.89 points (BH-adjusted p=.026) in the aggregate comparison.
- No significant advantage over any competitor was reported.
- Spiral-specific edge over RBF was +0.6 points and not significant; it did not transfer.
- Spiral phase response: 87.4% at zero phase, 87.6% at 0.25π, 91.8% at 0.50π, 98.7% at 0.75π, 99.0% at π.
- Random signs yielded 95.3%; random subsets/gains/incoherent settings were around 91.5%.
- Unit modulus mattered in those experiments, but complex representation itself was not essential.
- Redrawing phases with coordinates frozen dropped spiral accuracy from 100% to 54.3%; individual phase draws ranged from 26% to 83%.
- Joint retraining was identified as explaining why this did not contradict Study 2.
- Under shift/limited data, no advantage was observed; SVM was 80.7 versus Q-CIS 74.5.
- Runtime at 100 states: Q-CIS training 0.80s and 17ms/1000 queries versus 0.10s for RBF.

**Interpretation:** No demonstrated practical advantage; the model behaved like a kernel/random-feature-style classifier rather than a demonstrated new primitive.

## 16. Phase 4 — Mechanism and stability

Reported findings:
- Real-valued equivalent matched complex implementation to approximately $2.2\times10^{-16}$ and was about 3% faster.
- Across 13 datasets, complex Q-CIS tied RBF/SVM overall but lost by 14 percentage points on four concentric-rings experiments.
- Coordinate and phase sensitivity were similar under perturbation; phase was slightly more fragile for small perturbations.
- Full phase redraw accuracy was reported as 51.2% on spirals and 73.4% on moons.
- Regularisation improved redraw stability but at a steep accuracy cost.
- Parametric phases $\phi_i=s_i\cdot a+b$ were stable and near free-phase performance on moons, but cost 4.5 points on spirals and failed on rings.
- Joint initialisations agreed on 92.1% of predictions within 2 points.
- Frozen-coordinate phase refit recovered 56.7% of possible performance on spirals and 85.8% on moons.

**Interpretation:** Effects were dataset-specific, with instability in some conditions. The quantum-inspired framing was not necessary for the numerical implementation.

## 17. Phase 5 — Geometry and selection

Reported findings:
- Three frozen formulas were derived from 32 parameterisations; formulas were saved with SHA-256 hashes.
- Nonlinear-minus-linear probe gap correlated with phase benefit at rho=+.759, BH-adjusted p<.0001.
- Fisher ratio correlation was rho=−.688; linear separability correlation was rho=−.660.
- Held-out 12 parameterisations: gap rho=−.695, p=.012; Fisher ratio rho=−.606, p=.037.
- The first selector failed: 75% development leave-one-family-out accuracy, held-out 7/12=58.3%, binomial p=.774, and no gain over always-coherent.
- Initial bank contained few harmful cases; oracle advantage was only +0.15 points.
- Across 32 datasets, phase interference was never materially harmful under the reported threshold; worst −1.50, 19 ties within ±2, and 13 wins; mean +4.97.
- Classical baselines were better calibrated, had fewer parameters, and SVM was reported 76× faster.
- A known defect was identified: `linear_sep` used training accuracy and overfit at high dimension; this was not fixed after the held-out results in that phase.

**Interpretation:** A geometry association was observed, but the first selection rule did not generalize adequately. The training-accuracy linear-separability feature was problematic.

## 18. Phase 6 — Independent geometry validation

Reported findings:
- Phase 5 artifacts and frozen formulas were confirmed before new data.
- 24 new dataset families and 600 fits were evaluated.
- Frozen stump chose the better mechanism correctly on 19/20 non-tie families (95%, binomial p<.0001).
- It disabled phases on all four harmful families.
- Selector beat always-coherent by +0.56 points, reported p=.0047 at the then-used fit-level analysis; it captured 95% of oracle gain (+0.59).
- Nonlinear-minus-linear gap rho=+.772, p<.0001, replicating Phase 5.
- Linear separability was weaker (−.463, p=.023); Fisher ratio dropped out (−.381, p=.066).
- Four harmful families included a d=20 shell task: coherent 51.0, incoherent 58.2, RBF 96.0; frozen stump disabled phases.
- Q-CIS remained behind RBF by 4.34 points, SVM by 4.17, and MLP by 2.29, with p<.0001 reported for these comparisons.
- Training-set linear separability overfit at high dimension; cross-validated version was needed.

**Interpretation:** The geometry-gap relationship replicated in this bank, and the frozen selector classified mechanism choice well on this evaluation. However, Q-CIS remained behind conventional baselines overall.

## 19. Phase 7 — Cross-validated geometry prediction

Reported design:
- Corrected features were computed on 56 existing datasets (Phases 5–6) as development data.
- Both probes used stratified 5-fold cross-validation; linear-probe regularization was selected from {0.01, 0.1, 1, 10} using the same CV.
- Three formulas were frozen before the new bank:
  - D1: stump on `cv_gap`, threshold 0.0727.
  - D2: least-squares line $\Delta=0.0144+0.2592\cdot cv\_gap$.
  - D3: stump on CV linear probe; polarity was corrected before evaluation generation, with correction recorded.

New evaluation bank:
- 18 dataset families, 450 fits.
- 6 high-dimensional tasks (d=10–40).
- 5 noisy tasks (including 40% label noise, low SNR, heteroscedasticity, 10% informative labels, and heavy tails).
- 7 unseen geometries (interleaved parabolas, ring-vs-arc, swiss roll, nested squares, Voronoi tiling, 3D helices, and rotated crescents).

Reported results:
- `cv_gap` rho=+.491, p=.038; training gap rho=+.583, p=.011. Their difference was not established as statistically distinguishable.
- D1 selector accuracy 16/18 (88.9%, p=.0013); training-gap stump 15/18 (83.3%, p=.0075).
- Policy accuracy was 84.44% versus 84.39%.
- CV linear feature rho=−.037, p=.88; training linear feature −.220, p=.38.
- CV 1-NN rho=+.588.
- Six harmful families, four high-dimensional; high-dimensional block mean −1.31 points, within-block rho=−.314.
- Stump got 5/6 harmful-family decisions correct, largely because its default was off; this does not necessarily mean it tracked geometry within that subgroup.
- D2 regression decision rule accuracy was 55.6%, near chance. D3 was also weak.
- Selector was 83.88%? The original record reports selector 84.44%, always-coherent 83.88%, always-incoherent 82.49%, RBF 86.47%.
- The selector's +0.56-point difference over always-coherent was initially reported with a fit-level p-value; the later audit corrected the inferential unit.
- Oracle remained behind RBF by 1.51 points in that report.

**Interpretation before audit:** Geometry–benefit relationship appeared reproducible, and frozen threshold generalised on this bank, but there was no demonstrated practical advantage over RBF.

## 20. Phase 7 statistical audit — corrected inference

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

# Part IV — Consolidated interpretation

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

## 23. Known limitations and open questions

1. **Novelty:** A full literature review is required to determine whether the combination is distinct from known normalized RBF expansions, rank-one quadratic readouts, complex-valued models, and prototype methods.
2. **Baseline performance:** Conventional methods often performed better and were faster or better calibrated.
3. **Dataset dependence:** Results varied sharply across geometries; concentric rings and high-dimensional shell-like tasks exposed weaknesses.
4. **Phase instability:** Frozen-coordinate phase redraws could cause large performance drops.
5. **Selector utility:** Correctly predicting which mechanism wins on a family does not guarantee a useful accuracy gain.
6. **Statistical power:** Phase 7 has 18 independent families; confidence intervals are wide for some comparisons.
7. **Multiple comparisons:** The p=.028 selector-versus-always-incoherent contrast requires careful multiplicity context.
8. **Reproducibility:** Full code, data-generation routines, configurations, raw fits, and audit scripts must be published before independent reproduction is possible.
9. **Scaling:** State retrieval and distance calculations may scale with number of states and dimensionality; further profiling is needed.
10. **State relationships:** Class grouping and overlapping/context-dependent state membership require principled definitions.
11. **Feedback quality:** Incorrect or noisy feedback can reinforce bad states; confidence-aware updates and noisy-label tests remain important.
12. **Learned encoder confound:** A learned encoder could obscure whether gains come from Q-CIS's state/phase mechanism or conventional representation learning.

## 24. Public-release contents and recommended repository structure

Suggested repository:

```text
Q-CIS/
├── README.md
├── LICENSE
├── CITATION.cff
├── RESEARCH_SUMMARY.md
├── MATHEMATICAL_MODEL.md
├── METHODOLOGY.md
├── RESULTS_SUMMARY.md
├── LIMITATIONS.md
├── docs/
│   ├── original_proposal.md
│   ├── phase_history.md
│   └── statistical_audit_summary.md
├── src/                 # only after actual source is reviewed
├── tests/               # only actual tests
└── examples/             # only validated examples
```

Do not create placeholder source code and imply it is the implementation. If implementation files are unavailable, say so clearly.

## 25. Licence and attribution

The chosen public licence is the MIT License. It permits use, modification, redistribution, sublicensing, and commercial use, subject to preservation of the copyright and licence notice.

Recommended copyright attribution:

`Copyright (c) 2026 Adarsh K. B.`

The licence does not establish scientific validity or authorship of third-party components. Before publishing source code, inspect dependencies, assets, copied snippets, and third-party licences.

## 26. Contact and research enquiries

For additional experimental information, supporting results, or research enquiries, contact:

**adarsh.alford@gmail.com**

Suggested public note:

> This repository contains a partial public research release and selected reported findings. The complete experimental archive and some supporting materials are not included. If you would like additional experimental details, supporting results, or have questions about the methodology, please contact adarsh.alford@gmail.com.

---

# Part V — Release checklist for the uploading agent

- [ ] Preserve the MIT licence and use the abbreviated public attribution above.
- [ ] Publish this dossier or split it into the repository files listed above.
- [ ] Ensure README clearly says the release is partial and raw data/source are not included.
- [ ] Do not invent source code, datasets, plots, or benchmark results.
- [ ] Keep private raw fit-level data and internal archive out of the public repository unless separately approved.
- [ ] Verify every reported number against the original Phase 1–7 records before final publication.
- [ ] Ensure no school, phone number, home address, or other private identifying details are included.
- [ ] Test all Markdown equations and links after upload.
- [ ] Add a version/date and commit hash for the published release.
- [ ] If actual source code is added later, include dependency versions, environment instructions, tests, deterministic seeds, and a reproducibility guide.

---

## Source basis and provenance

This dossier uses the original project file **Project_QI_QCIS_Research_Proposal_v0.1.md** (uploaded to the user's Library on 8 November 2026) for the initial architecture, motivation, proposed equations, research questions, ablations, risks, and roadmap.

The Phases 1–7 experimental history and Phase 7 audit figures are based on the project's recorded research history in the conversation. The full Phase 1–7 raw archive and the audit package were not available as attached files during preparation of this dossier. Accordingly, those findings are explicitly labelled author-reported and should be checked against the original archived reports before publication.
