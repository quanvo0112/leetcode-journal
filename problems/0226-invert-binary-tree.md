# 0226. Invert Binary Tree

- **Problem Link:** https://leetcode.com/problems/invert-binary-tree/
- **Difficulty:** `Easy`
- **NeetCode Category:** `Trees`
- **LeetCode Topics:** `Tree` / `Depth-First Search` / `Breadth-First Search` / `Binary Tree`
- **Core Pattern:** `Recursive DFS / Pre-Order Subtree Pointer Swapping`
- **Last Practiced:** 2026-10-03
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - Given the `root` of a binary tree, invert the tree, and return its root.
  - Inverting means reflecting the tree across its vertical axis (a mirror image).
  - Constraints: Number of nodes in the range $[0, 100]$, node values $[-100, 100]$.
- **Core intuition:**
  - Trees are recursive data structures. The operation of inverting a binary tree decomposes naturally into the identical subproblem on its subtrees:
    1. For the current node, swap its left child pointer with its right child pointer.
    2. Recursively invert the left subtree (which was previously the right subtree).
    3. Recursively invert the right subtree (which was previously the left subtree).
  - **Base Case:** An empty subtree (`!root`) has no children to invert; return `nullptr` immediately.
  - **In-Place Mutation:** Pointers are modified in-place directly on the existing `TreeNode` structures. Returning `root` provides the correct entry point to the mirrored tree.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Iterative BFS / Level-Order Traversal ($O(N)$ time, $O(W)$ space):**
   - Push `root` into a `std::queue<TreeNode*>`.
   - While queue is non-empty: pop current node, swap `node->left` and `node->right`, push non-null children into the queue.
   - *Trade-off:* Prevents call stack overflow on extremely deep trees, but requires an auxiliary queue container allocating up to $O(N/2)$ nodes for the tree's maximum width.

2. **Approach 2 — Recursive DFS (Chosen Optimal Solution):**
   - Base case: `if (!root) return nullptr;`.
   - Action: `std::swap(root->left, root->right);`.
   - Recursive step: `invertTree(root->left); invertTree(root->right);`.
   - Return: `return root;`.
   - *Verdict:* Optimal $O(N)$ time and $O(h)$ auxiliary stack memory. Cleanest, most idiomatic tree traversal representation without external container allocation.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$
  - Where $N$ is the total number of nodes in the binary tree.
  - Every node is visited exactly once, performing an $O(1)$ constant-time pointer swap (`std::swap`).
- **Space Complexity:** $O(h)$
  - Where $h$ is the height of the tree, representing the maximum call stack depth.
  - **Best / Balanced Case:** $h = O(\log N)$ for balanced binary trees.
  - **Worst Case:** $h = O(N)$ for completely skewed (linked-list-like) trees.
  - Auxiliary heap allocation is strictly $O(1)$.

---

## 4. Edge Cases & Gotchas

- [x] **Empty Tree (`root == nullptr`):** Handled cleanly by the base condition `if (!root) return nullptr;`.
- [x] **Single-Node Tree:** Leaves have both children as `nullptr`; swapping two null pointers is safe and leaves the tree intact.
- [x] **Asymmetric / Skewed Subtrees:** A node with only a left child correctly moves that child to the right, and vice versa.
- [x] **Traversal Order Invariant:** Swapping before recursion (Pre-order DFS) is the most intuitive. If swapping after recursion (Post-order DFS), both subtrees must be fully inverted before their root pointers are swapped. Pre-order avoids temporary variable confusion.

---

## 5. Clean Code (Optimal Solution: Recursive DFS)

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
    TreeNode* invertTree(TreeNode* root) {
        if (!root) {
            return nullptr;
        }

        // Swap the left and right children of current node
        swap(root->left, root->right);

        // Recursively invert both subtrees
        invertTree(root->left);
        invertTree(root->right);

        return root;
    }
};
```

---

## 6. Review & Takeaways

### Visual Tree Reflection

```text
Original Tree:
         4
       /   \
      2     7
     / \   / \
    1   3 6   9

Step 1: Swap children of root (4)
         4
       /   \
      7     2
     / \   / \
    6   9 1   3

Step 2: Recurse into left child (7) and swap its children (6 <-> 9)
Step 3: Recurse into right child (2) and swap its children (1 <-> 3)

Final Inverted Tree:
         4
       /   \
      7     2
     / \   / \
    9   6 3   1
```

---

### The Architectural Mental Model

```text
                           Invert Binary Tree (root)
                                      ↓
                               root == nullptr ?
                                   /     \
                             YES  /       \  NO
                                 ↓         ↓
                           return nullptr  swap(root->left, root->right)
                                                  ↓
                                           invertTree(root->left)
                                                  ↓
                                           invertTree(root->right)
                                                  ↓
                                           return root
```

* **Next Review Date:** As needed / TBD
* **Key Takeaway:** Inverting a tree is purely recursive self-reflection: swap the current node's left and right children, then delegate the inversion to both subtrees.
