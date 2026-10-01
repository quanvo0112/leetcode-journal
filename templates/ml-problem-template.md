# [ML Problem Name]

- **Problem Link:** [NeetCode ML URL](https://neetcode.io/practice/machine-learning)
- **Difficulty:** `Easy` | `Medium` | `Hard`
- **NeetCode ML Module:** `Math Foundations` | `Build a Neural Net` | `PyTorch` | `Training` | `NLP` | `Attention & Transformers` | `Build GPT`
- **Implementation Framework:** `Python` / `NumPy` / `PyTorch`
- **Core Concept / Formulation:** `[e.g., Matrix Calculus, Cross-Entropy Loss, Self-Attention, LayerNorm]`
- **Last Practiced:** YYYY-MM-DD
- **Proficiency Level:**
  - [ ] Level 1: Solved smoothly (< 20 mins, vectorized, optimal)
  - [ ] Level 2: Struggled / Non-vectorized / Shape or dimension mismatch bugs
  - [ ] Level 3: Needed editorial or mathematical derivation hints

---

## 1. Mathematical Formulation & Derivations

- **Objective / Problem Statement:**
  > Concise description of what function, module, or training loop is being constructed from scratch.
- **Key Equations & Loss Functions:**
  $$\mathcal{L} = \dots$$
- **Analytical Gradients (Backpropagation / Matrix Derivatives):**
  $$\frac{\partial \mathcal{L}}{\partial W} = \dots$$
  $$\frac{\partial \mathcal{L}}{\partial b} = \dots$$

---

## 2. Tensor Shapes & Dimension Architecture

| Variable / Tensor | Symbol | Shape / Dimensions | Description |
|:---:|:---:|:---:|:---|
| Input Batch | $X$ | `(B, D_in)` | Batch of input features |
| Weight Matrix | $W$ | `(D_in, D_out)` | Linear projection weights |
| Bias Vector | $b$ | `(D_out,)` | Additive bias |
| Layer Output | $Y$ | `(B, D_out)` | Projected activations |

---

## 3. Vectorized Implementation & Numerical Stability

1. **Why Pure Vectorization (No Python Loops):**
   - Vectorized operations leverage SIMD instructions and optimized BLAS / LAPACK libraries (e.g., OpenBLAS, MKL), achieving $10\times$–$100\times$ speedups over standard Python `for` loops.
2. **Numerical Stability Safeguards:**
   - Log-Sum-Exp Trick: $\log \sum_i e^{z_i} = c + \log \sum_i e^{z_i - c}$ where $c = \max(z)$ (prevents floating-point overflow).
   - Division / Log safety: Add small constant $\epsilon = 10^{-12}$ (e.g., $\log(y + \epsilon)$) to prevent $\log(0) = -\infty$.

---

## 4. Complexity Analysis

- **Time Complexity / Compute (FLOPs):** $O(...)$ — Explanation based on matrix multiplication and batch size.
- **Space Complexity / Activation Memory:** $O(...)$ — Explanation of tensor allocations and cached activations required for the backward pass.

---

## 5. Edge Cases & Gotchas

- [ ] **Broadcasting Quirks:** Ensure biases `(D,)` properly broadcast across batch dimension `(B, D)`.
- [ ] **Zero-dimensional / Scalar vs. 1D Tensor:** Check shape consistency when computing loss.
- [ ] **Gradient Accumulation & In-place Operations:** Avoid modifying tensors in-place that are needed for backward autograd.
- [ ] **Padding & Masking:** Handle causal masks or padding masks correctly in attention operations.

---

## 6. Clean Code

```python
import numpy as np

# Clean, production-quality NumPy or PyTorch implementation here
```

---

## 7. Architecture Walkthrough & Key Takeaways

```text
Input Tensor (B, D_in)
          ↓
  Matrix Multiplication  <--- Weights (D_in, D_out)
          ↓
     Add Bias (D_out,)
          ↓
  Activation Function (e.g., ReLU / Softmax)
          ↓
Output Tensor (B, D_out)
```

* **Next Review Date:** YYYY-MM-DD
* **Key Takeaway:** [One-sentence reusable mathematical intuition or vectorized implementation rule].
