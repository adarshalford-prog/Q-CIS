# References

Sources for the prior art behind each ingredient of Q-CIS. Every entry below was
checked against a publisher page, DOI record or the official proceedings listing
before being included; page ranges are given as the publisher records them. Nothing
here is cited from memory alone.

This list exists to make one point unavoidable: **the individual components of Q-CIS
are all established.** The open question is whether the *combination* is distinct, and
that question has not been settled.

---

## 1. Radial basis function networks

The class score in Q-CIS is a normalised squared-modulus expansion over Gaussian
similarities. That is RBF machinery.

1. **Broomhead, D. S., & Lowe, D. (1988).** Multivariable functional interpolation and
   adaptive networks. *Complex Systems*, 2(3), 321–355.
2. **Moody, J., & Darken, C. J. (1989).** Fast learning in networks of locally-tuned
   processing units. *Neural Computation*, 1(2), 281–294.
   DOI: [10.1162/neco.1989.1.2.281](https://doi.org/10.1162/neco.1989.1.2.281)

**Relevance.** Normalised Gaussian responses around centres, combined into a decision,
is precisely the RBF construction. The historical record itself reports Q-CIS losing
to RBF in aggregate, which is consistent with this overlap.

## 2. Prototype learning and learning vector quantisation

Moving internal states toward observations they should represent, and away from those
they confuse, is LVQ.

3. **Sato, A., & Yamada, K. (1995).** Generalized learning vector quantization.
   In *Advances in Neural Information Processing Systems 8* (NIPS 1995), pp. 423–429.
   MIT Press, 1996.
   <https://proceedings.neurips.cc/paper_files/paper/1995/hash/9c3b1830513cc3b8fc4b76635d32e692-Abstract.html>

**Relevance.** The attraction/repulsion rules described in the original Q-CIS proposal
are the LVQ family's learning rules. The proposal says as much. What would need to be
new is the *complete* learning rule including phase, not the attraction/repulsion idea.

## 3. Metric learning

A learned linear encoder feeding a geometric classifier is metric learning.

4. **Xing, E. P., Ng, A. Y., Jordan, M. I., & Russell, S. J. (2003).** Distance metric
   learning, with application to clustering with side-information. In *Advances in
   Neural Information Processing Systems 15* (NIPS 2002), pp. 521–528. MIT Press.
   (Some indexes record pp. 505–512 for this paper; the proceedings listing gives
   521–528.)
5. **Weinberger, K. Q., & Saul, L. K. (2009).** Distance metric learning for large
   margin nearest neighbor classification. *Journal of Machine Learning Research*,
   10, 207–244.
   <https://www.jmlr.org/papers/v10/weinberger09a.html>

**Relevance.** Q-CIS learns $$q = Wx$$, a global linear transformation of the input
space preceding a distance-based classifier. That is the LMNN formulation's starting
point. The encoder is therefore not a novel contribution of Q-CIS, and the proposal
correctly flags a learned encoder as a confound when attributing gains.

## 4. Complex-valued models and phase

Using complex amplitudes with phase is an established modelling choice, not a quantum
one.

6. **Hirose, A. (2012).** *Complex-Valued Neural Networks* (2nd ed.). Studies in
   Computational Intelligence, vol. 400. Springer, Berlin.
   DOI: [10.1007/978-3-642-27632-3](https://doi.org/10.1007/978-3-642-27632-3)
7. **Trabelsi, C., Bilaniuk, O., Zhang, Y., Serdyuk, D., Subramanian, S., Santos, J. F.,
   Mehri, S., Rostamzadeh, N., Bengio, Y., & Pal, C. J. (2018).** Deep complex
   networks. *International Conference on Learning Representations (ICLR 2018)*.
   <https://openreview.net/forum?id=H1T2hmZAb>

**Relevance.** Complex-valued networks with amplitude and phase are a mature field.
The specific finding in this project — that the squared modulus has an exact real
sine/cosine equivalent, so complex arithmetic buys nothing numerically — is a known
consequence of writing $$|z|^2 = (\Re z)^2 + (\Im z)^2$$, not a discovery.

## 5. Quantum-inspired machine learning and quantum probability

8. **Schuld, M., Sinayskiy, I., & Petruccione, F. (2015).** An introduction to quantum
   machine learning. *Contemporary Physics*, 56(2), 172–185.
   DOI: [10.1080/00107514.2014.964942](https://doi.org/10.1080/00107514.2014.964942)
9. **Pothos, E. M., & Busemeyer, J. R. (2013).** Can quantum probability provide a new
   direction for cognitive modeling? *Behavioral and Brain Sciences*, 36(3), 255–274.
   DOI: [10.1017/S0140525X12001525](https://doi.org/10.1017/S0140525X12001525)

**Relevance.** These establish what "quantum-inspired" legitimately means: either
algorithms for quantum hardware, or classical models borrowing the *probability
formalism*. Q-CIS is in neither category in any strong sense — it borrows complex
amplitudes and interference, then computes a score that has an exact real-valued
equivalent. Pothos and Busemeyer are also explicit that quantum probability models
are not always better than classical ones, which is the same caution this project's
own results point to.

## 6. Statistics

The Phase 7 correction — that the dataset family, not the seed-level fit, is the
independent unit — rests on standard methodology.

10. **Holm, S. (1979).** A simple sequentially rejective multiple test procedure.
    *Scandinavian Journal of Statistics*, 6(2), 65–70.
11. **Benjamini, Y., & Hochberg, Y. (1995).** Controlling the false discovery rate: a
    practical and powerful approach to multiple testing. *Journal of the Royal
    Statistical Society, Series B*, 57(1), 289–300.
    DOI: [10.1111/j.2517-6161.1995.tb02031.x](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x)

`src/qcis/stats.py` implements both corrections directly, and `tests/test_stats.py`
checks their monotonicity and bounds.

---

## What is already known

* Gaussian/RBF responses around centres, combined into a decision rule, are a
  long-established classifier family.
* Prototype movement rules with attraction and repulsion are the LVQ family.
* A learned linear input transformation before a geometric classifier is metric
  learning.
* Complex-valued networks with amplitude and phase are a mature field, and squared
  moduli always admit a real sine/cosine evaluation.
* Interference between complex amplitudes is a standard way to express
  order- and context-dependent probability in quantum-cognition models.
* Controlling multiplicity and choosing the correct independent unit are settled
  statistical practice, and ignoring them is a known way to manufacture significance.

## What remains unproven about Q-CIS

1. **Whether the combination is distinct.** No systematic literature review has been
   completed. Until one is, Q-CIS is a recombination of known parts, not a new method.
2. **Whether phase learning helps.** The historical record reports a small, mostly
   non-significant effect that did not survive the family-level correction. This
   release's reference implementation finds the same direction of answer on newly
   generated data.
3. **Whether the selector is useful.** Correctly predicting which mechanism wins on a
   family does not deliver a meaningful accuracy gain, and the audit found the
   selector-vs-always-coherent contrast indistinguishable from zero.
4. **Whether any of it beats a well-tuned classical baseline.** The record says no; the
   reference implementation here also does not beat a Gaussian-kernel ridge baseline.

## What this release does not claim

No quantum advantage, no physical quantum computation, no entanglement, no new
computational primitive, no general superiority over RBF, SVM, MLP or neural
networks, no general-purpose intelligence, no long-term memory or reasoning, and no
independent reproducibility of the historical figures.

Combining known mathematical components does not by itself make a contribution
original. Establishing that would require the literature review and the comparisons
that this project has not yet completed.
