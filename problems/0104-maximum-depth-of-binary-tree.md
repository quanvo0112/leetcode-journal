# 0104. Maximum Depth of Binary Tree

- **Problem Link:** https://leetcode.com/problems/maximum-depth-of-binary-tree/
- **Difficulty:** `Easy`
- **NeetCode Category:** `Trees`
- **LeetCode Topics:** `Tree` / `Depth-First Search` / `Breadth-First Search` / `Binary Tree`
- **Core Pattern:** `Post-Order Recursive DFS / Divide and Conquer Depth Aggregation`
- **Last Practiced:** 2026-10-03
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - Given the `root` of a binary tree, return its maximum depth.
  - Maximum depth is defined as the number of nodes along the longest path from the root node down to the farthest leaf node.
  - Constraints: Number of nodes in $[0, 10^4]$, node values in $[-100, 100]$.
- **Core intuition:**
  - The maximum depth of any binary tree rooted at `node` decomposes naturally into the depths of its two subtrees:
    $$\text{depth}(node) = 1 + \max(\text{depth}(node.left), \text{depth}(node.right))$$
  - **Base Case:** An empty subtree (`!root`) has a depth of $0$.
  - **Bottom-Up Post-Order Paradigm:**
    - In contrast to top-down pre-order traversal (like **LeetCode 0226 Invert Binary Tree**, where mutations happen before recursing), this problem exemplifies **bottom-up post-order aggregation**:
      1. Query left subtree for its depth.
      2. Query right subtree for its depth.
      3. Combine child information at the current node by taking $\max(\text{left}, \text{right}) + 1$.
  - **Zero External State Variables:**
    - There is no need to maintain a global variable or pass accumulators down the recursion frames. Each recursive function call directly returns the intrinsic depth of its own rooted subtree.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Iterative BFS / Level-Order Traversal ($O(N)$ time, $O(W)$ space):**
   - Push `root` into a `std::queue<TreeNode*>`. Process nodes level-by-level using an inner loop of size `q.size()`, incrementing `depth` after each level.
   - *Trade-off:* Avoids deep call stack frames on skewed trees, but requires an auxiliary queue allocating up to $O(N/2)$ memory for the maximum level width.

2. **Approach 2 — Iterative DFS with Explicit Stack ($O(N)$ time, $O(h)$ space):**
   - Maintain `std::stack<pair<TreeNode*, int>>` storing node and its current depth, updating a global maximum.
   - *Trade-off:* Simulates call stack explicitly, but introduces verbose boilerplate code.

3. **Approach 3 — Post-Order Recursive DFS (Chosen Optimal Solution):**
   - Base case: `if (!root) return 0;`.
   - Recurse: `return 1 + max(maxDepth(root->left), maxDepth(root->right));`.
   - *Verdict:* Optimal $O(N)$ time and $O(h)$ auxiliary stack memory. Pure functional tree decomposition with minimal syntax and zero external data structure overhead.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$
  - Where $N$ is the total number of nodes in the binary tree.
  - Every node is visited exactly once, performing constant-time $O(1)$ operations (`max` and addition).
- **Space Complexity:** $O(h)$
  - Where $h$ represents the height of the tree, determining the maximum call stack depth.
  - **Best / Balanced Case:** $h = O(\log N)$ for balanced binary trees.
  - **Worst Case:** $h = O(N)$ for completely degenerate (skewed/linked-list-like) trees.
  - Auxiliary heap allocation is strictly $O(1)$.

---

## 4. Edge Cases & Gotchas

- [x] **Empty Tree (`root == nullptr`):** Handled cleanly by the base condition `if (!root) return 0;`.
- [x] **Single-Node Tree:** Both child calls return $0$; current node evaluates $1 + \max(0, 0) = 1$.
- [x] **Unbalanced / Skewed Tree:** If all nodes extend along a single branch (e.g., only left children), the non-empty branch contributes its full height while the empty branch contributes $0$, correctly returning $N$.

---

## 5. Clean Code (Optimal Solution: Post-Order Recursive DFS)

```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    int maxDepth(TreeNode* root) {
        if (!root) {
            return 0;
        }

        return 1 + max(maxDepth(root->left),
                       maxDepth(root->right));
    }
};
```

---

## 6. Review & Takeaways

### Visual Bottom-Up Reduction

```text
Given Tree:
          3
        /   \
       9     20
            /  \
           15   7

Bottom-Up Depth Propagation:
- Leaf 9:   left=0, right=0  --> 1 + max(0, 0) = 1
- Leaf 15:  left=0, right=0  --> 1 + max(0, 0) = 1
- Leaf 7:   left=0, right=0  --> 1 + max(0, 0) = 1
- Node 20:  left=1, right=1  --> 1 + max(1, 1) = 2
- Root 3:   left=1, right=2  --> 1 + max(1, 2) = 3

Return Result: 3
```

---

### The Architectural Mental Model

```text
                     Maximum Depth of Binary Tree
                                  ↓
                          root == nullptr ?
                              /       \
                        YES  /         \  NO
                            ↓           ↓
                        return 0    Recurse Subtrees:
                                    leftDepth  = maxDepth(root->left)
                                    rightDepth = maxDepth(root->right)
                                        ↓
                                    Combine at Parent:
                                    return 1 + max(leftDepth, rightDepth)
```

* **Next Review Date:** As needed / TBD
* **Key Takeaway:** Tree depth aggregation is the canonical bottom-up divide-and-conquer pattern: compute the metric on both children, combine them with `max()`, and add $1$ for the current node.
