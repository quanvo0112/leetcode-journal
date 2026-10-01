# Gradient Descent

- **Problem Link:** [NeetCode - Gradient Descent](https://neetcode.io/problems/gradient-descent)
- **Difficulty:** `Easy`
- **NeetCode ML Module:** `Math Foundations`
- **Implementation Framework:** `Python`
- **Core Concept / Formulation:** `First-Order Optimization, Gradient Descent, Scalar Derivatives, Learning Rate Update Rule`
- **Last Practiced:** 2026-10-01
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, vectorized, optimal)
  - [ ] Level 2: Struggled / Non-vectorized / Shape or dimension mismatch bugs
  - [ ] Level 3: Needed editorial or mathematical derivation hints

---

## 1. Mathematical Formulation & Derivations

- **Objective / Problem Statement:**
  > Minimize the scalar quadratic function $f(x) = x^2$ using standard first-order Gradient Descent over a fixed number of iterations (`iterations`), starting from an initial scalar position `init` with a specified step size (`learning_rate`). The returned minimizer must be rounded to 5 decimal places (`round(..., 5)`).

- **Objective Function & Global Minimum:**
  $$f(x) = x^2$$
  Since $f(x)$ is strictly convex with a positive second derivative ($f''(x) = 2 > 0$), there exists a unique global minimum at:
  $$x^* = 0, \quad f(x^*) = 0$$

- **Analytical Derivative (Gradient):**
  $$\frac{df}{dx} = \nabla_x f(x) = 2x$$

- **Iterative Parameter Update Rule:**
  In Gradient Descent, parameters are updated in the direction of steepest descent (the negative gradient) scaled by the learning rate $\eta$:
  $$x^{(t+1)} = x^{(t)} - \eta \cdot \frac{df}{dx}\Big|_{x^{(t)}}$$
  Substituting $\frac{df}{dx} = 2x$:
  $$x^{(t+1)} = x^{(t)} - \eta \cdot (2x^{(t)}) = x^{(t)}(1 - 2\eta)$$

---

## 2. Tensor Shapes & Dimension Architecture

| Variable / Parameter | Symbol | Shape / Type | Description |
|:---:|:---:|:---:|:---|
| Current Minimizer | $x$ | `float` (Scalar) | Value of $x$ being iteratively updated |
| Gradient / Derivative | $g$ | `float` (Scalar) | First derivative $\frac{df}{dx} = 2x$ |
| Learning Rate | $\eta$ | `float` (Scalar) | Step size scaling factor (`learning_rate`) |
| Iterations | $T$ | `int` (Scalar) | Total number of descent update steps |

---

## 3. Vectorized Implementation & Numerical Stability

1. **Sequential Nature of Time Steps:**
   - Because each optimization step depends explicitly on the state from the previous step ($x^{(t+1)} = f(x^{(t)})$), the temporal iteration loop `for _ in range(iterations):` is inherently sequential.
   - For this scalar single-variable problem, external libraries like NumPy or PyTorch are unnecessary; native Python floating-point operations provide optimal performance without memory overhead.
2. **Convergence & Stability Invariant:**
   - Unfolding the recurrence relation yields $x^{(T)} = x^{(0)} \cdot (1 - 2\eta)^T$.
   - **Convergence Condition:** The sequence converges to $x^* = 0$ if and only if $|1 - 2\eta| < 1$, which requires $0 < \eta < 1$.
   - For standard small learning rates (e.g., $\eta = 0.01$), the contraction factor is $1 - 2(0.01) = 0.98 < 1$, guaranteeing smooth geometric contraction toward the origin.
   - If $\eta \ge 1$, the updates overshoot and diverge ($|1 - 2\eta| \ge 1$).

---

## 4. Complexity Analysis

- **Time Complexity:** $O(\text{iterations})$ — The loop executes exactly $T$ iterations, performing $O(1)$ scalar multiplications and subtractions per step.
- **Space Complexity:** $O(1)$ — Optimization is performed in-place using a single scalar variable `x` without allocating auxiliary data structures.

---

## 5. Edge Cases & Gotchas

- [x] **Initial Value at Global Minimum ($x = 0$):** Gradient is $2 \times 0 = 0$; $x$ remains strictly $0.0$.
- [x] **Zero Iterations (`iterations = 0`):** The loop body is skipped; returns `round(init, 5)`.
- [x] **Negative Initial Values ($x < 0$):** Gradient is negative ($g < 0$). Subtracting a negative gradient increases $x$ in the positive direction toward $0$.
- [x] **Precision & Rounding:** Floating-point operations accumulate slight precision variances. The problem strictly requires `round(x, 5)` before returning.

---

## 6. Clean Code

```python
class Solution:
    def get_minimizer(self, iterations: int, learning_rate: float, init: int) -> float:
        x = float(init)
        for _ in range(iterations):
            gradient = 2 * x
            x -= learning_rate * gradient
        return round(x, 5)
```

---

## 7. Architecture Walkthrough & Key Takeaways

### Visual Step-by-Step Simulation

```text
Given: init = 5, learning_rate = 0.01, iterations = 10

Iteration 0: x = 5.0
Iteration 1: gradient = 2 * 5.0 = 10.0  --> x = 5.0 - (0.01 * 10.0) = 4.90000
Iteration 2: gradient = 2 * 4.9 = 9.8   --> x = 4.9 - (0.01 * 9.8)  = 4.80200
Iteration 3: gradient = 2 * 4.802 = 9.604 --> x = 4.802 - (0.01 * 9.604) = 4.70596
...
Iteration 10: x = 4.08536...
Final Result: round(4.08536..., 5) = 4.08536
```

### Architectural Mental Model

```text
       Initial Parameter (init)
                  ↓
  ┌───────────────────────────────────────────────┐
  │ For t = 1 to iterations:                      │
  │   1. Compute Gradient: g = 2 * x              │
  │   2. Parameter Update: x = x - learning_rate*g│
  └───────────────────────────────────────────────┘
                  ↓
     Round to 5 Decimal Places
                  ↓
             Return x
```

* **Next Review Date:** 2026-10-08
* **Key Takeaway:** All machine learning optimization reduces to the foundational rule $\theta \leftarrow \theta - \eta \cdot \nabla_\theta \mathcal{L}$; whether optimizing a single scalar or billions of neural network weights, only the dimensionality of the gradient changes from scalar to multidimensional tensor.
