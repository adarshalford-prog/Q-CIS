# Q-CIS — Reported experimental history (Phases 1–7)

> **Important.** These values and descriptions are transcribed from the project's recorded
> research history. They are not independently recalculated in this document because the raw data
> and executable analysis archive are not published. The record as transcribed runs Phase 1,
> Phase 3, Phase 4, Phase 5, Phase 6, Phase 7; a Phase 2 write-up was not present in the source.

---

## 1. Phase 1 — Initial prototype, ablations, and corrections

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

## 2. Phase 3 — Independent reproduction and falsification

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

## 3. Phase 4 — Mechanism and stability

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

## 4. Phase 5 — Geometry and selection

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

## 5. Phase 6 — Independent geometry validation

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

## 6. Phase 7 — Cross-validated geometry prediction

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
