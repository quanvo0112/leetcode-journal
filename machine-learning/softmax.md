# Softmax

- **Problem Link:** [NeetCode - Softmax](https://neetcode.io/problems/softmax)
- **Difficulty:** `Easy`
- **NeetCode ML Module:** `Math Foundations`
- **Implementation Framework:** `NumPy`
- **Core Concept / Formulation:** `Activation Functions, Probability Distribution, Numerical Stability, Max Subtraction Trick, SIMD Vectorization`
- **Last Practiced:** 2026-10-02
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, vectorized, optimal)
  - [ ] Level 2: Struggled / Non-vectorized / Shape or dimension mismatch bugs
  - [ ] Level 3: Needed editorial or mathematical derivation hints

---

## 1. Mathematical Formulation & Derivations

- **Objective / Problem Statement:**
  > Given a 1D NumPy array $z \in \mathbb{R}^n$ representing unnormalized logit scores, implement the **Softmax** activation function to transform $z$ into a valid categorical probability distribution $\sigma(z) \in (0, 1)^n$ such that $\sum_{i=1}^n \sigma(z)_i = 1$. The returned probabilities must be rounded element-wise to 4 decimal places (`np.round(..., 4)`).

- **Standard Softmax Formulation:**
  $$\sigma(z)_i = \frac{e^{z_i}}{\sum_{j=1}^n e^{z_j}}$$

- **The Numerical Overflow Hazard:**
  - In IEEE 754 double-precision floating-point arithmetic (`float64`), $e^{z}$ overflows to infinity (`np.inf`) whenever $z_i \gtrsim 709.78$.
  - When any logit exceeds this bound, the naive formulation evaluates to:
    $$\frac{\infty}{\infty} \longrightarrow \text{NaN}$$
  - This numerical instability causes forward-pass breakdown and gradient vanishing/exploding during neural network training.

- **Mathematical Shift Invariance (The Max Subtraction Trick):**
  - Softmax is strictly invariant to uniform additive shifts. Let $c = \max(z)$ be an arbitrary scalar shift:
    $$\frac{e^{z_i - c}}{\sum_{j=1}^n e^{z_j - c}} = \frac{e^{z_i} \cdot e^{-c}}{\sum_{j=1}^n (e^{z_j} \cdot e^{-c})} = \frac{e^{z_i} \cdot e^{-c}}{e^{-c} \cdot \sum_{j=1}^n e^{z_j}} = \frac{e^{z_i}}{\sum_{j=1}^n e^{z_j}}$$
  - **Guaranteed Stability Invariant:** By setting $c = \max_{j} z_j$, every shifted logit satisfies:
    $$z_i - \max(z) \le 0 \quad \forall i \in \{1, \dots, n\}$$
  - Consequently:
    $$e^{z_i - \max(z)} \in (0, 1]$$
  - The maximum shifted exponent is strictly $e^0 = 1.0$, completely eliminating floating-point overflow while keeping the normalization sum bounded away from 0 ($\sum_j e^{z_j - c} \ge 1.0$), which also prevents division by zero.

---

## 2. Tensor Shapes & Dimension Architecture

| Variable / Tensor | Symbol | Shape / Type | Description |
|:---:|:---:|:---:|:---|
| Input Logits | $z$ | `NDArray[np.float64]` of shape `(N,)` | 1D array of unnormalized real-valued logits |
| Maximum Scalar | $c = \max(z)$ | `np.float64` (Scalar) | Maximum logit value across the array |
| Shifted Exponentials | $\exp(z - c)$ | `NDArray[np.float64]` of shape `(N,)` | Stable exponential activations in range $(0, 1]$ |
| Partition Function (Sum) | $\sum_j \exp(z_j - c)$ | `np.float64` (Scalar) | Normalizing denominator |
| Output Probabilities | $\sigma(z)$ | `NDArray[np.float64]` of shape `(N,)` | Categorical probabilities summing to 1.0 |

---

## 3. Vectorized Implementation & Numerical Stability

1. **NumPy Vectorization (No Python Loops):**
   - Rather than iterating over elements with a Python loop, operations (`np.max`, subtraction, `np.exp`, `np.sum`, division) execute sequentially in compiled C/BLAS kernels.
   - Vectorization leverages CPU SIMD instruction pipelines, achieving $10\times$–$100\times$ speedups.
2. **Broadcasting Mechanism:**
   - `z - np.max(z)` automatically broadcasts the scalar maximum across the 1D vector `z` in-place of shape `(N,)`.
   - `exp_z / np.sum(exp_z)` divides the 1D vector by the scalar partition function.
3. **Rounding Invariant:**
   - Per problem specifications, the resulting probabilities are rounded to 4 decimal places via `np.round(..., 4)`.

---

## 4. Complexity Analysis

- **Time Complexity:** $O(N)$
  - `np.max(z)` performs a single linear pass: $O(N)$.
  - `z - np.max(z)` performs element-wise subtraction: $O(N)$.
  - `np.exp(...)` evaluates $N$ exponential operations: $O(N)$.
  - `np.sum(...)` accumulates $N$ elements: $O(N)$.
  - Element-wise division and rounding take $O(N)$ operations.
  - Overall Time: $O(N)$ where $N$ is the number of logits.
- **Space Complexity:** $O(N)$
  - Allocates intermediate array `exp_z` and return array of shape `(N,)`.
  - Auxiliary memory overhead is strictly $O(N)$ without recursive call frames.

---

## 5. Edge Cases & Gotchas

- [x] **Large Positive Logits ($z = [1000.0, 1001.0, 1002.0]$):**
  - Without max subtraction: $e^{1000} \to \infty \implies \text{NaN}$.
  - With max subtraction: shifted logits become $[-2.0, -1.0, 0.0]$, yielding completely stable probabilities without overflow.
- [x] **Large Negative Logits ($z = [-1000.0, -1001.0, -1002.0]$):**
  - Max subtraction shifts values to $[0.0, -1.0, -2.0]$, ensuring the denominator is at least $e^0 = 1.0$ (never division by zero).
- [x] **Identical Logits ($z = [k, k, k]$):**
  - Shifts to $[0, 0, 0] \implies e^0 = 1 \implies [1/3, 1/3, 1/3] = [0.3333, 0.3333, 0.3333]$.
- [x] **Rounding Precision:** Must round to **4 decimal places** (`np.round(..., 4)`) as specified in the problem template.

---

## 6. Clean Code

```python
import numpy as np
from numpy.typing import NDArray

class Solution:
    def softmax(self, z: NDArray[np.float64]) -> NDArray[np.float64]:
        exp_z = np.exp(z - np.max(z))
        return np.round(exp_z / np.sum(exp_z), 4)
```

---

## 7. Architecture Walkthrough & Key Takeaways

### Visual Step-by-Step Simulation

```text
Input: z = [1.0, 2.0, 3.0]

Step 1: Compute Maximum
  max(z) = 3.0

Step 2: Subtract Maximum (Shift)
  z - max(z) = [-2.0, -1.0, 0.0]

Step 3: Exponentiate
  exp_z = [e^(-2), e^(-1), e^(0)]
        = [0.135335, 0.367879, 1.000000]

Step 4: Sum of Exponentials (Denominator)
  sum(exp_z) = 0.135335 + 0.367879 + 1.000000 = 1.503214

Step 5: Normalize Probabilities
  exp_z / sum = [0.090031, 0.244728, 0.665240]

Step 6: Round to 4 Decimals
  np.round(..., 4) = [0.09, 0.2447, 0.6652]
  Sum of probabilities ≈ 1.0
```

---

### Architectural Pipeline

```text
               Unnormalized Logits: z ∈ R^N
                            ↓
               Find Maximum: c = np.max(z)
                            ↓
           Shifted Logits: z_shift = z - c  (≤ 0)
                            ↓
         Bounded Exponents: exp_z = np.exp(z_shift)  (∈ (0, 1])
                            ↓
           Partition Sum: S = np.sum(exp_z)  (≥ 1.0)
                            ↓
          Normalized Distribution: P = exp_z / S
                            ↓
           Element-wise Round: np.round(P, 4)
                            ↓
               Valid Categorical Distribution
```

* **Next Review Date:** As needed / TBD
* **Key Takeaway:** Always apply the max-subtraction trick ($z - \max(z)$) prior to exponentiation to guarantee numerical stability; Softmax is shift-invariant and serves as the universal categorical probability operator across classification heads, cross-entropy loss, and transformer self-attention ($\text{softmax}(QK^T / \sqrt{d_k})$).
