# Linear Regression (Forward)

- **Problem Link:** [NeetCode - Linear Regression Forward](https://neetcode.io/problems/linear-regression-forward)
- **Difficulty:** `Easy`
- **NeetCode ML Module:** `Math Foundations`
- **Implementation Framework:** `NumPy`
- **Core Concept / Formulation:** `Linear Regression, Forward Pass, Matrix-Vector Multiplication, Mean Squared Error (MSE), Vectorized Loss`
- **Last Practiced:** 2026-10-03
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, vectorized, optimal)
  - [ ] Level 2: Struggled / Non-vectorized / Shape or dimension mismatch bugs
  - [ ] Level 3: Needed editorial or mathematical derivation hints

---

## 1. Mathematical Formulation & Derivations

- **Objective / Problem Statement:**
  > Implement the forward inference pass and error metric for standard **Linear Regression** using NumPy. Given a design matrix of input features $X \in \mathbb{R}^{n \times m}$ and a parameter weight vector $w \in \mathbb{R}^m$, compute the model predictions $\hat{y}$ rounded to 5 decimal places (`np.round(..., 5)`). Given predictions $\hat{y} \in \mathbb{R}^n$ and ground truth targets $y \in \mathbb{R}^n$, compute the **Mean Squared Error (MSE)** loss rounded to 5 decimal places (`round(..., 5)`).

- **1. Linear Hypothesis (Forward Projection):**
  $$\hat{y} = Xw$$
  For each sample $i \in \{1, \dots, n\}$ with feature row $x_i = [x_{i1}, x_{i2}, \dots, x_{im}]$:
  $$\hat{y}_i = \sum_{j=1}^m x_{ij} w_j = x_i \cdot w$$
  Expressed compactly in matrix notation via the Python `@` matrix multiplication operator:
  $$\hat{y} = X @ w \in \mathbb{R}^n$$

- **2. Mean Squared Error (MSE) Objective:**
  $$\text{MSE}(\hat{y}, y) = \frac{1}{n} \sum_{i=1}^n (\hat{y}_i - y_i)^2$$
  - Measures the average squared Euclidean distance between predicted and true responses.
  - Strictly convex with respect to parameters $w$, facilitating guaranteed convergence under gradient descent.

---

## 2. Tensor Shapes & Dimension Architecture

| Variable / Tensor | Symbol | Shape / Type | Description |
|:---:|:---:|:---:|:---|
| Input Feature Matrix | $X$ | `NDArray[np.float64]` of shape `(n, m)` | Batch of $n$ samples, each with $m$ features |
| Weight Vector | $w$ | `NDArray[np.float64]` of shape `(m,)` | Linear model parameters |
| Predicted Vector | $\hat{y}$ | `NDArray[np.float64]` of shape `(n,)` | Model output predictions (`X @ weights`) |
| Ground Truth Vector | $y$ | `NDArray[np.float64]` of shape `(n,)` | Actual continuous target labels |
| Residual Vector | $\hat{y} - y$ | `NDArray[np.float64]` of shape `(n,)` | Element-wise prediction error |
| Scalar Error | $\text{MSE}$ | `float` (Scalar) | Mean squared residual across all $n$ samples |

---

## 3. Vectorized Implementation & Numerical Stability

1. **Matrix Multiplication (`@` Operator):**
   - The matrix-vector dot product `X @ weights` compiles to BLAS `dgemv` (double-precision general matrix-vector multiply) routines.
   - Executes across multiple CPU SIMD vector lanes, eliminating nested Python loops and achieving maximal throughput.
2. **Element-wise Difference & Squaring:**
   - `(model_prediction - ground_truth) ** 2` performs element-wise subtraction and squaring in a contiguous memory block without temporary list allocations.
3. **Foundation for Deep Learning & Transformers:**
   - The linear projection $\hat{y} = Xw$ represents the foundational linear transformation $Y = XW$ pervasive across Dense / Linear layers, Multi-Layer Perceptrons (MLPs), and Transformer projection heads ($Q = XW_Q, K = XW_K, V = XW_V$).

---

## 4. Complexity Analysis

- **Time Complexity:**
  - `get_model_prediction`: $O(n \cdot m)$ — Multiplies an $(n \times m)$ matrix by an $(m \times 1)$ vector, requiring $n \times m$ multiplications and additions.
  - `get_error`: $O(n)$ — Evaluates $n$ subtractions, $n$ squares, and a single mean reduction.
  - Overall Forward Pass: $O(n \cdot m)$.
- **Space Complexity:**
  - `get_model_prediction`: $O(n)$ auxiliary memory to allocate the output prediction vector `(n,)`.
  - `get_error`: $O(n)$ auxiliary memory for the intermediate squared residual array before scalar reduction.

---

## 5. Edge Cases & Gotchas

- [x] **1D vs. 2D Weight Vector:**
  - When `weights` has shape `(m,)`, NumPy treats it as a 1D vector and produces output shape `(n,)` directly without needing `reshape` or `squeeze`.
- [x] **Zero Error ($y_{\text{true}} = y_{\text{pred}}$):**
  - Residuals are strictly $0.0$, yielding $\text{MSE} = 0.0$.
- [x] **Rounding Specifications:**
  - Predictions array is rounded via `np.round(predictions, 5)`.
  - Loss scalar is rounded via Python's built-in `round(mse, 5)`.

---

## 6. Clean Code

```python
import numpy as np
from numpy.typing import NDArray

class Solution:
    def get_model_prediction(
        self, X: NDArray[np.float64], weights: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        predictions = X @ weights
        return np.round(predictions, 5)

    def get_error(
        self, model_prediction: NDArray[np.float64], ground_truth: NDArray[np.float64]
    ) -> float:
        mse = np.mean((model_prediction - ground_truth) ** 2)
        return round(mse, 5)
```

---

## 7. Architecture Walkthrough & Key Takeaways

### Visual Computation Flow

```text
Input Matrix X (2, 2):
[[1.0, 2.0],
 [3.0, 4.0]]

Weights w (2,):
[10.0, 20.0]

Step 1: Forward Prediction (X @ w)
  Row 0: 1.0 * 10.0 + 2.0 * 20.0 = 50.0
  Row 1: 3.0 * 10.0 + 4.0 * 20.0 = 110.0
  predictions = [50.0, 110.0]

Step 2: MSE Error Evaluation (Ground Truth = [55.0, 100.0])
  Residuals: [50.0 - 55.0, 110.0 - 100.0] = [-5.0, 10.0]
  Squared:   [(-5.0)^2, (10.0)^2]          = [25.0, 100.0]
  Mean:      (25.0 + 100.0) / 2            = 62.5
```

---

### Architectural Pipeline

```text
  Design Matrix X (n, m) ──┐
                           ├───>  Matrix Multiply: X @ w  ───>  Predictions ŷ (n,)
  Weights w (m,) ──────────┘                                             │
                                                                         ▼
  Ground Truth y (n,)    ─────────────────────────────────────>  MSE = mean((ŷ - y)²)
                                                                         │
                                                                         ▼
                                                                  Scalar Loss (MSE)
```

* **Next Review Date:** As needed / TBD
* **Key Takeaway:** Forward propagation in linear models is simply matrix-vector multiplication $\hat{y} = Xw$, followed by the Mean Squared Error metric measuring average squared residuals across the batch.
