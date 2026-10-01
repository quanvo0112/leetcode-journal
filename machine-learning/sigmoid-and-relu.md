# Sigmoid & ReLU

- **Problem Link:** [NeetCode - Sigmoid & ReLU](https://neetcode.io/problems/sigmoid-and-relu)
- **Difficulty:** `Easy`
- **NeetCode ML Module:** `Math Foundations`
- **Implementation Framework:** `NumPy`
- **Core Concept / Formulation:** `Activation Functions, Element-Wise Operations, Vectorization, Sigmoid, Rectified Linear Unit (ReLU)`
- **Last Practiced:** 2026-10-01
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, vectorized, optimal)
  - [ ] Level 2: Struggled / Non-vectorized / Shape or dimension mismatch bugs
  - [ ] Level 3: Needed editorial or mathematical derivation hints

---

## 1. Mathematical Formulation & Derivations

- **Objective / Problem Statement:**
  > Implement two foundational non-linear activation functions in deep learning: **Sigmoid** ($\sigma(z)$) and **Rectified Linear Unit** ($\text{ReLU}(z)$). Both functions must operate element-wise over a 1D NumPy array `z` containing real values (`np.float64`). Sigmoid values must be rounded to 5 decimal places (`np.round(..., 5)`).

- **1. Sigmoid Function:**
  $$\sigma(z) = \frac{1}{1 + e^{-z}}$$
  - Maps any real number $z \in (-\infty, \infty)$ strictly into the open interval $(0, 1)$, widely utilized for Bernoulli probability estimation in binary classification and gating mechanisms (e.g., LSTMs, GRUs).
  - Symmetry: $\sigma(-z) = 1 - \sigma(z)$ with inflection point at $\sigma(0) = 0.5$.
  - First Derivative:
    $$\frac{d\sigma}{dz} = \sigma(z)(1 - \sigma(z))$$

- **2. Rectified Linear Unit (ReLU) Function:**
  $$\text{ReLU}(z) = \max(0, z) = \begin{cases} z & \text{if } z > 0 \\ 0 & \text{if } z \le 0 \end{cases}$$
  - Provides piecewise linearity that introduces non-linearity without suffering from vanishing gradients in positive saturation regimes ($\frac{d}{dz}\text{ReLU}(z) = 1$ for $z > 0$).
  - Subgradient:
    $$\frac{d}{dz}\text{ReLU}(z) = \begin{cases} 1 & \text{if } z > 0 \\ 0 & \text{if } z < 0 \end{cases}$$

---

## 2. Tensor Shapes & Dimension Architecture

| Variable / Tensor | Symbol | Shape / Type | Description |
|:---:|:---:|:---:|:---|
| Input Array | $z$ | `NDArray[np.float64]` of shape `(N,)` | 1D pre-activation array |
| Sigmoid Output | $\sigma(z)$ | `NDArray[np.float64]` of shape `(N,)` | Probabilities bounded in $(0, 1)$ |
| ReLU Output | $\text{ReLU}(z)$ | `NDArray[np.float64]` of shape `(N,)` | Non-negative rectified activations |

---

## 3. Vectorized Implementation & Numerical Stability

1. **NumPy Vectorization (No Python Loops):**
   - In neural networks, activations are computed over millions of tensor elements per forward pass. Using Python `for` loops introduces heavy interpreter overhead and boxing/unboxing costs.
   - Native NumPy operations (`np.exp`, `np.maximum`, `np.round`) dispatch directly to compiled C kernels leveraging CPU SIMD vector lanes (AVX2 / AVX-512), executing orders of magnitude faster.
2. **`np.maximum` vs. `np.max` vs. Built-in `max`:**
   - Python built-in `max(0, z)` fails on NumPy arrays because truth values of multidimensional arrays are ambiguous.
   - `np.max(z)` performs a full array reduction, returning a single scalar maximum across all elements.
   - `np.maximum(0, z)` performs element-wise maximum comparison by broadcasting scalar `0` across every element of `z`.
3. **Rounding Invariant:**
   - Per problem specifications, the output of `sigmoid(z)` is rounded element-wise using `np.round(..., 5)`.

---

## 4. Complexity Analysis

- **Time Complexity:**
  - `sigmoid`: $O(N)$ — Performs element-wise arithmetic (negation, exponential, addition, division, rounding) across $N$ elements.
  - `relu`: $O(N)$ — Evaluates element-wise maximum across $N$ elements.
- **Space Complexity:**
  - $O(N)$ auxiliary space — Allocates a new output array of shape `(N,)` for the activations, avoiding in-place mutation of the input tensor.

---

## 5. Edge Cases & Gotchas

- [x] **Zero Value ($z = 0$):**
  - $\sigma(0) = \frac{1}{1 + 1} = 0.5$
  - $\text{ReLU}(0) = \max(0, 0) = 0.0$
- [x] **Extreme Positive Inputs ($z \to +\infty$):**
  - $\lim_{z \to \infty} \sigma(z) = 1.0$
  - $\text{ReLU}(z) = z$
- [x] **Extreme Negative Inputs ($z \to -\infty$):**
  - $\lim_{z \to -\infty} \sigma(z) = 0.0$
  - $\text{ReLU}(z) = 0.0$
- [x] **Data Type Integrity:** Return arrays maintain `NDArray[np.float64]` precision.

---

## 6. Clean Code

```python
import numpy as np
from numpy.typing import NDArray

class Solution:
    def sigmoid(self, z: NDArray[np.float64]) -> NDArray[np.float64]:
        return np.round(1 / (1 + np.exp(-z)), 5)

    def relu(self, z: NDArray[np.float64]) -> NDArray[np.float64]:
        return np.maximum(0, z)
```

---

## 7. Architecture Walkthrough & Key Takeaways

### Visual Traces

```text
Example 1: Sigmoid Activation
Input z:        [-2.0,       0.0,      2.0]
-z:             [ 2.0,       0.0,     -2.0]
exp(-z):        [ 7.38906,   1.0,      0.13534]
1 + exp(-z):    [ 8.38906,   2.0,      1.13534]
1 / (...):      [ 0.11920,   0.50000,  0.88080]
np.round(...,5):[ 0.1192,    0.5,      0.8808]

Example 2: ReLU Activation
Input z:        [-2.0, -1.0, 0.0, 3.0]
np.maximum(0,z):[ 0.0,  0.0, 0.0, 3.0]
```

### Architectural Pipeline

```text
       Pre-activation Vector z: NDArray[float64] (N,)
                             ↓
       ┌─────────────────────┴─────────────────────┐
       │                                           │
  [ Sigmoid Path ]                            [ ReLU Path ]
       ↓                                           ↓
  np.exp(-z)                                 np.maximum(0, z)
       ↓                                           ↓
  1 / (1 + exp(-z))                                │
       ↓                                           │
  np.round(..., 5)                                 │
       ↓                                           ↓
  Output: (N,) in (0, 1)                      Output: (N,) in [0, ∞)
```

* **Next Review Date:** As needed / TBD
* **Key Takeaway:** Always use vectorized SIMD primitives (`np.exp`, `np.maximum`, `np.round`) rather than Python loops or built-in `max()`; element-wise broadcasting forms the backbone of all forward and backward neural network layers.
