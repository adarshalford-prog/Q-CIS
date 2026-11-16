# Q-CIS — Limitations and open questions

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

---

## Contact

Additional experimental information, supporting results, and research enquiries:
**adarsh.alford@gmail.com**
