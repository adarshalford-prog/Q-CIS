# Q-CIS — Mathematical model

The proposed architecture, the later classifier formulation, the real-valued equivalent, and the
interpretation boundary.

> **Status note.** The original proposal is a research plan. The later formulation in Part II
> describes the experimental classifier actually used. The complex notation is a mathematical
> representation on classical hardware; it does not establish physical quantum superposition,
> entanglement, or quantum advantage.

---

## 1. Proposed architecture

The initial proposed pipeline is:

**Input → Coordinate encoding → Candidate-state retrieval → Complex amplitude assignment → Interference-based decision → Feedback → Coordinate and phase updates → Persistent state memory**

### 1.1 Coordinate state space

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

### 1.2 Complex-valued amplitudes and phases

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

### 1.3 Interference-based decision

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

### 1.4 Coordinate-based learning

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

### 1.5 Phase-based learning

The phase can be updated using a loss gradient:

$$
\phi_i^{(t+1)}=\phi_i^{(t)}-\eta_\phi\frac{\partial L}{\partial\phi_i}
$$

Where $\eta_\phi$ is the phase learning rate.

The phase update should be wrapped modulo $2\pi$, and numerical stability must be checked.

The hypothesis is that phase updates can improve the way competing candidate states combine. This is not guaranteed. The system must be tested against an otherwise identical model with phases fixed, randomized, or removed.

### 1.6 Combined learning cycle

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

## 2. Later classifier formulation

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

### 2.1 Real-valued equivalent

The same class score can be computed without complex arithmetic:

$$
z_c=
\left(\sum_{i\in I_c}r_i\cos\phi_i\right)^2+
\left(\sum_{i\in I_c}r_i\sin\phi_i\right)^2
$$

The reported real-valued and complex implementations matched to approximately $2.2\times10^{-16}$ in the tested implementation. The real-valued version was reported to be about 3% faster in the Phase 4 comparison. Complex arithmetic is not essential to compute this score.

### 2.2 Interpretation boundary

This is a classical normalized squared-modulus RBF-style expansion / rank-one quadratic readout. The use of complex notation does not establish physical quantum superposition, entanglement, or quantum advantage. The method's ingredients overlap with established areas including embeddings, metric learning, RBF methods, prototype learning, and complex-valued models.

No claim of a new computational primitive is made.

---

## 3. Existing equivalents and related research

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

---

## Further reading

- Research questions and interpretation: [RESEARCH_SUMMARY.md](RESEARCH_SUMMARY.md)
- Experimental plan: [METHODOLOGY.md](METHODOLOGY.md)
