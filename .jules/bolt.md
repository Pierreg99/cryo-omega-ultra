
## 2024-05-24 - Lexical search bottleneck

**Learning:** The default cosine similarity implementation over `Counter` objects computed the dot product over the union of keys (`set(a) | set(b)`), leading to an O(M+N) cost and many zero multiplications. Furthermore, computing vector magnitudes inside the loop dynamically for the query adds a massive constant overhead to the `_cosine` execution.

**Action:** Calculate the dot product only by iterating over keys present in both vectors, effectively doing `sum(a[k]*b[k] for k in a if k in b)`. If dot product is zero, return early without doing the costly math.sqrt calculations. And finally, when applying this in a search context (`semantic.search`), pre-compute the magnitude of the query vector *once* outside of the search loop, and pass it in to `_cosine` for every iteration.
