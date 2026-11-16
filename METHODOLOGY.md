# Q-CIS — Methodology

The experimental plan from the original proposal, the v0.1 prototype specification, the
development roadmap, and the protocol behind the reported phases.

> **Status note.** Sections 7–10 describe the *planned* protocol and prototype target. The
> reported Phase 1–7 runs followed this design, but the full configurations, code, and raw data
> are not included in this release, so the protocol cannot be re-executed from these documents
> alone.

---

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

---

## Further reading

- Reported results: [RESULTS_SUMMARY.md](RESULTS_SUMMARY.md)
- Full phase-by-phase record: [docs/phase_history.md](docs/phase_history.md)
- Statistical audit: [docs/statistical_audit_summary.md](docs/statistical_audit_summary.md)
