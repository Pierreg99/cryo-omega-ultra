## 2025-05-19 - Fast TF-Cosine
**Learning:** In lexical retrieval operations, cosine similarity can be a bottleneck. Creating unions of dictionary keys (`set(a) | set(b)`) for sparse vectors is highly inefficient because it is $O(|A| + |B|)$ and allocates memory for sets.
**Action:** Iterate over the smaller dict using `len(a) > len(b)` swapping and checking `b.get(k, 0)` for O(min(|A|, |B|)) dot products. Introduce early exits (e.g. `if dot == 0: return 0.0`) to skip heavy denominator calculation.
