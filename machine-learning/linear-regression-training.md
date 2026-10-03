# Linear Regression (Training)

- **Problem Link:** [NeetCode - Linear Regression Training](https://neetcode.io/problems/linear-regression-training)
- **Difficulty:** `Medium`
- **NeetCode ML Module:** `Math Foundations`
- **Implementation Framework:** `NumPy`
- **Core Concept / Formulation:** `Supervised Learning, Gradient Descent Training Loop, Mean Squared Error Partial Derivatives, Batch Optimization`
- **Last Practiced:** 2026-10-03
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, vectorized, optimal)
  - [ ] Level 2: Struggled / Non-vectorized / Shape or dimension mismatch bugs
  - [ ] Level 3: Needed editorial or mathematical derivation hints

---

## 1. Mathematical Formulation & Derivations

- **Objective / Problem Statement:**
  > Implement the complete iterative **Gradient Descent** optimization loop to train a Linear Regression model from scratch. Given input features $X \in \mathbb{R}^{N \times M}$, continuous ground truth targets $Y \in \mathbb{R}^N$, total training iterations $K$ (`num_iterations`), and initial parameter weights $w_0 \in \mathbb{R}^M$, iteratively update $w$ using analytical MSE partial derivatives and fixed learning rate $\eta = 0.01$. Return the final optimized weights rounded to 5 decimal places (`np.round(..., 5)`).

- **1. Mean Squared Error (MSE) Objective:**
  $$\mathcal{L}(w) = \frac{1}{N} \sum_{i=1}^N (\hat{y}_i - y_i)^2 = \frac{1}{N} \sum_{i=1}^N \left( \sum_{j=1}^M X_{ij} w_j - y_i \right)^2$$

- **2. Analytical Gradient Derivation (Partial Derivatives):**
  Applying the chain rule with respect to each individual weight parameter $w_j$:
  $$\frac{\partial \mathcal{L}}{\partial w_j} = \frac{1}{N} \sum_{i=1}^N 2(\hat{y}_i - y_i) \cdot \frac{\partial (\hat{y}_i - y_i)}{\partial w_j}$$
  Since $\frac{\partial \hat{y}_i}{\partial w_j} = X_{ij}$:
  $$\frac{\partial \mathcal{L}}{\partial w_j} = \frac{2}{N} \sum_{i=1}^N (\hat{y}_i - y_i) X_{ij} = -\frac{2}{N} \sum_{i=1}^N (y_i - \hat{y}_i) X_{ij}$$
  Expressed as a vector dot product between the prediction error vector and the $j$-th feature column $X_{:, j}$:
  $$\nabla_{w_j} \mathcal{L} = -\frac{2}{N} (Y - \hat{Y}) \cdot X_{:, j}$$

- **3. Parameter Update Rule:**
  At each training iteration step:
  $$w_j^{(t+1)} = w_j^{(t)} - \eta \cdot \frac{\partial \mathcal{L}}{\partial w_j}$$

---

## 2. Tensor Shapes & Dimension Architecture

| Variable / Tensor | Symbol | Shape / Type | Description |
|:---:|:---:|:---:|:---|
| Training Design Matrix | $X$ | `NDArray[np.float64]` of shape `(N, M)` | $N$ training examples with $M$ feature dimensions |
| Target Labels | $Y$ | `NDArray[np.float64]` of shape `(N,)` | Ground truth continuous target labels |
| Weight Vector | $w$ | `NDArray[np.float64]` of shape `(M,)` | Model weights updated iteratively |
| Model Predictions | $\hat{Y}$ | `NDArray[np.float64]` of shape `(N,)` | Batch predictions: $\hat{Y} = X @ w$ |
| Feature Column | $X_{:, j}$ | `NDArray[np.float64]` of shape `(N,)` | $j$-th feature across all $N$ examples |
| Partial Derivative | $\frac{\partial \mathcal{L}}{\partial w_j}$ | `float` (Scalar) | Gradient of MSE with respect to weight $w_j$ |

---

## 3. Vectorized Implementation & Numerical Stability

1. **Decoupled Forward & Backward Passes:**
   - In each iteration, `model_prediction = self.get_model_prediction(X, weights)` is computed once upfront in $O(N \cdot M)$ time.
   - Recomputing predictions inside the inner weight loop would uselessly multiply complexity by $M$ ($O(N \cdot M^2)$). Caching predictions ensures the loop runs in $O(N \cdot M)$ per iteration.
2. **Immutability of Caller Inputs (`copy()`):**
   - `weights = initial_weights.copy()` creates an independent mutable copy of the weights, preventing side-effects from mutating the caller's array in-place.
3. **Synthesis of Track Primitives:**
   - This problem unites the entire **Math Foundations** module:
     $$\text{Forward Pass (LC 5)} \longrightarrow \text{MSE Derivative} \longrightarrow \text{Gradient Descent Loop (LC 1)}$$
   - Forms the complete archetype for all downstream neural network training loops, backpropagation passes, and mini-batch optimizers.

---

## 4. Complexity Analysis

- **Time Complexity:** $O(K \cdot N \cdot M)$
  - Let $K$ be `num_iterations`, $N$ be the number of samples (`len(X)`), and $M$ be the number of weights/features (`len(weights)`).
  - Forward pass per iteration: $X @ w \implies O(N \cdot M)$.
  - Gradient computation per iteration: $M$ dot products of length $N \implies M \times O(N) = O(N \cdot M)$.
  - Total Time: $K \times (O(N \cdot M) + O(N \cdot M)) = O(K \cdot N \cdot M)$.
- **Space Complexity:** $O(N + M)$
  - Allocates `weights` copy of size $M$ and intermediate `model_prediction` array of size $N$.
  - Auxiliary memory overhead is strictly $O(N + M)$.

---

## 5. Edge Cases & Gotchas

- [x] **In-Place Mutation Bug:** Modifying `initial_weights` directly without `.copy()` pollutes input state across multiple training calls.
- [x] **Negative Sign in Derivative:**
  - Notice the formulation: $-2 \cdot (Y - \hat{Y}) \cdot X_{:, j} / N$.
  - Alternatively: $2 \cdot (\hat{Y} - Y) \cdot X_{:, j} / N$. Both are mathematically identical.
- [x] **Rounding Specification:** Weights are rounded element-wise to 5 decimal places (`np.round(weights, 5)`).

---

## 6. Clean Code

```python
import numpy as np
from numpy.typing import NDArray

class Solution:
    def get_derivative(
        self,
        model_prediction: NDArray[np.float64],
        ground_truth: NDArray[np.float64],
        N: int,
        X: NDArray[np.float64],
        desired_weight: int,
    ) -> float:
        return -2 * np.dot(
            ground_truth - model_prediction, X[:, desired_weight]
        ) / N

    def get_model_prediction(
        self, X: NDArray[np.float64], weights: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        return np.squeeze(np.matmul(X, weights))

    learning_rate = 0.01

    def train_model(
        self,
        X: NDArray[np.float64],
        Y: NDArray[np.float64],
        num_iterations: int,
        initial_weights: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        weights = initial_weights.copy()
        N = len(X)

        for _ in range(num_iterations):
            model_prediction = self.get_model_prediction(X, weights)
            for j in range(len(weights)):
                gradient = self.get_derivative(
                    model_prediction, Y, N, X, j
                )
                weights[j] -= self.learning_rate * gradient

        return np.round(weights, 5)
```

---

## 7. Architecture Walkthrough & Key Takeaways

### Visual Training Loop Execution

```text
Initialize: weights = initial_weights.copy()

┌─────────────────────────────────────────────────────────────┐
│ For step = 1 to num_iterations:                             │
│                                                             │
│   1. Forward Pass (Batch Prediction):                       │
│      model_prediction = X @ weights           shape: (N,)   │
│                                                             │
│   2. Backward Pass (Compute Gradients):                     │
│      For each feature j = 0 to M - 1:                       │
│        g_j = -2 * dot(Y - model_prediction, X[:, j]) / N    │
│                                                             │
│   3. Optimization Step (Gradient Descent):                  │
│      weights[j] = weights[j] - learning_rate * g_j         │
└─────────────────────────────────────────────────────────────┘
                              ↓
              Final Output: np.round(weights, 5)
```

---

### The Architectural Mental Model

```text
                  Math Foundations (Complete Pipeline)
                                    ↓
       Forward Pass (LC 5) ───> ŷ = X @ w
                                    ↓
        Loss Metric (LC 4) ───> MSE = mean((y - ŷ)²)
                                    ↓
    Analytical Gradient (LC 6) ───> ∇_w MSE = -2/N (y - ŷ) @ X
                                    ↓
  Gradient Descent Update (LC 1) ───> w ← w - η * ∇_w MSE
                                    ↓
                       Trained Linear Regressor
```

* **Next Review Date:** As needed / TBD
* **Key Takeaway:** A training loop consists of forward evaluation ($Xw$), error residual calculation ($Y - \hat{Y}$), gradient projection onto feature columns ($X_{:, j}$), and descent step ($w \leftarrow w - \eta \cdot g$); caching batch predictions upfront prevents $O(M^2)$ recomputations.
