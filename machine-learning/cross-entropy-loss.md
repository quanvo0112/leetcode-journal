# Cross-Entropy Loss

- **Problem Link:** [NeetCode - Cross-Entropy Loss](https://neetcode.io/problems/cross-entropy-loss)
- **Difficulty:** `Easy`
- **NeetCode ML Module:** `Math Foundations`
- **Implementation Framework:** `NumPy`
- **Core Concept / Formulation:** `Loss Functions, Binary Cross-Entropy (BCE), Categorical Cross-Entropy (CCE), Numerical Clipping, Vectorized Reduction`
- **Last Practiced:** 2026-10-02
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, vectorized, optimal)
  - [ ] Level 2: Struggled / Non-vectorized / Shape or dimension mismatch bugs
  - [ ] Level 3: Needed editorial or mathematical derivation hints

---

## 1. Mathematical Formulation & Derivations

- **Objective / Problem Statement:**
  > Implement two fundamental loss functions in supervised machine learning: **Binary Cross-Entropy (BCE)** for binary classification and **Categorical Cross-Entropy (CCE)** for multi-class classification with one-hot encoded targets. Both functions must operate over NumPy arrays with numerical clipping against extreme values ($10^{-7}, 1 - 10^{-7}$) and return scalar loss values rounded to 4 decimal places (`round(loss, 4)`).

- **1. Binary Cross-Entropy Loss (BCE):**
  - Paired natively with **Sigmoid** activation $\sigma(z) \in (0, 1)$.
  - Given ground truth $y \in \{0, 1\}^n$ and predicted probabilities $\hat{y} \in (0, 1)^n$:
    $$\mathcal{L}_{\text{BCE}} = -\frac{1}{n} \sum_{i=1}^n \left[ y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i) \right]$$
  - When $y_i = 1$, the penalty is $-\log(\hat{y}_i)$; as $\hat{y}_i \to 0$, loss $\to \infty$.
  - When $y_i = 0$, the penalty is $-\log(1 - \hat{y}_i)$; as $\hat{y}_i \to 1$, loss $\to \infty$.

- **2. Categorical Cross-Entropy Loss (CCE):**
  - Paired natively with **Softmax** activation across $c$ mutually exclusive classes.
  - Given one-hot encoded targets $Y \in \{0, 1\}^{n \times c}$ and predicted distributions $\hat{Y} \in (0, 1)^{n \times c}$:
    $$\mathcal{L}_{\text{CCE}} = -\frac{1}{n} \sum_{i=1}^n \sum_{j=1}^c Y_{ij} \log(\hat{Y}_{ij})$$
  - Because $Y_i$ is one-hot (only the true label index $k$ has $Y_{ik} = 1$), this collapses to the negative log-likelihood of the correct class:
    $$\mathcal{L}_i = -\log(\hat{Y}_{i, \text{true\_class}})$$

- **3. Numerical Stability Safeguard (`np.clip`):**
  - $\log(0)$ is mathematically undefined ($\lim_{x \to 0^+} \log(x) = -\infty$).
  - If a model outputs confident but incorrect predictions ($\hat{y} = 0$ when $y = 1$), $\log(\hat{y})$ evaluates to `-\inf`, producing `NaN` or infinite losses.
  - Clipping predictions to $[\epsilon, 1 - \epsilon]$ where $\epsilon = 10^{-7}$ prevents infinite losses while preserving precision:
    $$\hat{y}_{\text{clipped}} = \text{clip}(\hat{y}, 10^{-7}, 1 - 10^{-7})$$

---

## 2. Tensor Shapes & Dimension Architecture

| Variable / Tensor | Symbol | Shape / Type | Description |
|:---:|:---:|:---:|:---|
| BCE True Labels | $y_{\text{true}}$ | `NDArray[np.float64]` of shape `(N,)` | 1D ground-truth binary targets $\{0, 1\}$ |
| BCE Predictions | $y_{\text{pred}}$ | `NDArray[np.float64]` of shape `(N,)` | 1D predicted probabilities in $(0, 1)$ |
| CCE True Labels | $Y_{\text{true}}$ | `NDArray[np.float64]` of shape `(N, C)` | 2D one-hot target matrix ($N$ samples, $C$ classes) |
| CCE Predictions | $Y_{\text{pred}}$ | `NDArray[np.float64]` of shape `(N, C)` | 2D Softmax probability distribution matrix |
| Sample Losses (CCE) | $\mathcal{L}_{\text{sample}}$ | `NDArray[np.float64]` of shape `(N,)` | Row-wise sum across classes (`axis=1`) |
| Final Scalar Loss | $\mathcal{L}$ | `float` (Scalar) | Batch-averaged loss rounded to 4 decimals |

---

## 3. Vectorized Implementation & Numerical Stability

1. **Pure Vectorization without Loops:**
   - Both formulas avoid nested Python loops by computing element-wise Hadamard products ($Y \odot \log \hat{Y}$) directly in C/BLAS memory.
2. **Two-Stage CCE Reduction (`axis=1` followed by `np.mean`):**
   - `np.sum(y_true * np.log(y_pred), axis=1)` compresses the $(N, C)$ matrix along class dimension $C$ into an $N$-length vector containing the loss per sample.
   - `-np.mean(...)` computes the average across all $N$ samples in the batch.
3. **The Canonical Neural Network Pairs:**
   - **Sigmoid $\rightarrow$ Binary Cross-Entropy:** Foundation for binary classification, multi-label classification, and logistic regression.
   - **Softmax $\rightarrow$ Categorical Cross-Entropy:** Foundation for multi-class classification and Autoregressive Language Models (GPT).

---

## 4. Complexity Analysis

- **Time Complexity:**
  - **BCE:** $O(N)$ — Evaluates clipping, element-wise products, logs, and mean over $N$ scalar targets.
  - **CCE:** $O(N \cdot C)$ — Evaluates clipping, log, element-wise matrix multiplication, and reductions across $N \times C$ entries.
- **Space Complexity:**
  - **BCE:** $O(N)$ auxiliary memory for allocating intermediate clipped arrays and log buffers.
  - **CCE:** $O(N \cdot C)$ auxiliary memory for allocating intermediate clipped array `(N, C)` and sample loss vector `(N,)`.

---

## 5. Edge Cases & Gotchas

- [x] **Extreme Confident Predictions ($\hat{y} = 0.0$ or $\hat{y} = 1.0$):**
  - Clipped safely to $10^{-7}$ and $1 - 10^{-7}$, avoiding $-\infty$ and `NaN`.
- [x] **Perfect Predictions ($y_{\text{true}} = y_{\text{pred}}$):**
  - Loss approaches $-\log(1 - 10^{-7}) \approx 0.0$.
- [x] **CCE Reduction Axis:**
  - Sum must be taken over `axis=1` (across classes per sample) before averaging across samples (`np.mean`), preserving the mathematical definition.
- [x] **Precision & Rounding:** Return value is a Python `float` rounded to 4 decimal places via `round(loss, 4)`.

---

## 6. Clean Code

```python
import numpy as np
from numpy.typing import NDArray

class Solution:
    def binary_cross_entropy(
        self, y_true: NDArray[np.float64], y_pred: NDArray[np.float64]
    ) -> float:
        y_pred = np.clip(y_pred, 1e-7, 1 - 1e-7)
        loss = -np.mean(
            y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred)
        )
        return round(loss, 4)

    def categorical_cross_entropy(
        self, y_true: NDArray[np.float64], y_pred: NDArray[np.float64]
    ) -> float:
        y_pred = np.clip(y_pred, 1e-7, 1 - 1e-7)
        loss = -np.mean(
            np.sum(y_true * np.log(y_pred), axis=1)
        )
        return round(loss, 4)
```

---

## 7. Architecture Walkthrough & Key Takeaways

### Visual Computation Flow

```text
Binary Cross-Entropy (BCE):
y_true: [1.0, 0.0]
y_pred: [0.9, 0.2]
  ↓
y_true * log(y_pred)        = [1.0 * log(0.9), 0.0 * ...]       = [-0.1054,  0.0000]
(1 - y_true) * log(1 - pred) = [0.0 * ...,       1.0 * log(0.8)] = [ 0.0000, -0.2231]
Sum per sample:             = [-0.1054, -0.2231]
Mean across batch:          = -0.16425
Negate & Round:             = 0.1643

Categorical Cross-Entropy (CCE):
y_true: [[1, 0, 0], [0, 1, 0]]  (N=2, C=3)
y_pred: [[0.7, 0.2, 0.1], [0.1, 0.8, 0.1]]
  ↓
y_true * log(y_pred):
  Row 0: [1 * log(0.7), 0, 0] = [-0.3567, 0, 0]
  Row 1: [0, 1 * log(0.8), 0] = [0, -0.2231, 0]
Sum axis=1 (per sample):    = [-0.3567, -0.2231]
Mean across batch:          = -0.2899
Negate & Round:             = 0.2899
```

---

### Architectural Mental Model

```text
  Activation Function                 Loss Formulation                      Target Application
  ───────────────────                 ────────────────                      ──────────────────
  Sigmoid σ(z) ∈ (0, 1)      ───>     Binary Cross-Entropy (BCE)     ───>   Binary / Multi-label Classification
  Softmax σ(z) ∈ Δ^{C-1}     ───>     Categorical Cross-Entropy (CCE) ───>  Multi-class Classification & GPT Next-Token
```

* **Next Review Date:** As needed / TBD
* **Key Takeaway:** Cross-entropy measures the divergence between true label distributions and predicted probabilities; always clip predictions to $[\epsilon, 1-\epsilon]$ to safeguard against $\log(0) = -\infty$, and pair Sigmoid with BCE and Softmax with CCE.
