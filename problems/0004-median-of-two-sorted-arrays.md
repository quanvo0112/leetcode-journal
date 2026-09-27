# 0004. Median of Two Sorted Arrays

- **Problem Link:** https://leetcode.com/problems/median-of-two-sorted-arrays/
- **Difficulty:** `Hard`
- **NeetCode Category:** `Binary Search`
- **LeetCode Topics:** `Array` / `Binary Search` / `Divide and Conquer`
- **Core Pattern:** `Binary Search on Partition (Cut Invariant on Smaller Array)`
- **Last Practiced:** 2026-09-27
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively.
  - Return the median of the two sorted arrays.
  - **Explicit Complexity Constraint:** The overall run time complexity must be $O(\log(m + n))$.
- **Core intuition:**
  - Finding the median does not require merging the arrays into an $O(m + n)$ buffer.
  - By definition, the median divides a sorted collection into two equal-sized halves:
    - Every element in the **left half** must be $\le$ every element in the **right half**.
  - If we cut `nums1` into two parts at index $i$ (taking $i$ elements into the left half) and cut `nums2` at index $j$ (taking $j$ elements into the left half), the total number of left-half elements is fixed:
    $$\text{half} = \frac{m + n + 1}{2}$$
  - Since $i + j = \text{half}$, choosing $i$ immediately determines $j = \text{half} - i$.
  - Therefore, the problem reduces to searching for a single cut point $i$ in `nums1`.
  - By ensuring `nums1` is the smaller array ($m \le n$), we search over a bounded range $[0, m]$, guaranteeing $O(\log(\min(m, n)))$ time and ensuring $j \ge 0$.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Merge and Sort ($O((m + n) \log(m + n))$ time, $O(m + n)$ space):**
   - Concatenate both arrays and call `std::sort`.
   - *Verdict:* Completely violates the $O(\log(m + n))$ requirement.

2. **Approach 2 — Two-Pointer Merge Simulation ($O(m + n)$ time, $O(1)$ space):**
   - Advance two pointers to simulate the merge until reaching index $(m + n) / 2$.
   - *Verdict:* Solves space constraint ($O(1)$), but linear time $O(m + n)$ still fails the required logarithmic bound.

3. **Approach 3 — Binary Search on Partition (Chosen Optimal Solution):**
   - Ensure `nums1.size() <= nums2.size()` by swapping arguments if necessary.
   - Total elements required in the left partition: `half = (m + n + 1) / 2`.
   - Define partition bounds: `left = max(0, half - n)`, `right = min(half, m)`.
   - Search for partition $i$:
     - $j = \text{half} - i$.
     - Identify border elements with sentinels:
       - $\text{left1} = (i == 0) \ ? \ \text{INT\_MIN} : \text{nums1}[i - 1]$
       - $\text{right1} = (i == m) \ ? \ \text{INT\_MAX} : \text{nums1}[i]$
       - $\text{left2} = (j == 0) \ ? \ \text{INT\_MIN} : \text{nums2}[j - 1]$
       - $\text{right2} = (j == n) \ ? \ \text{INT\_MAX} : \text{nums2}[j]$
     - **Check partition invariant:**
       - If $\text{left1} > \text{right2}$: cut in `nums1` is too far right $\implies \text{right} = i - 1$.
       - Else if $\text{left2} > \text{right1}$: cut in `nums1` is too far left $\implies \text{left} = i + 1$.
       - Else: correct partition found!
         - If $(m + n)$ is odd: median is $\max(\text{left1}, \text{left2})$.
         - If $(m + n)$ is even: median is $\frac{\max(\text{left1}, \text{left2}) + \min(\text{right1}, \text{right2})}{2.0}$.
   - *Verdict:* Meets the strict $O(\log(\min(m, n)))$ time bound with $O(1)$ auxiliary space.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(\log(\min(m, n)))$
  - Binary search is performed strictly over the partition index $i$ of the smaller array of size $m \le n$. Each iteration takes $O(1)$ comparisons.
- **Space Complexity:** $O(1)$
  - Only integer pointers, sentinels, and boundary indices are allocated. No dynamic structures are created.

---

## 4. Edge Cases & Gotchas

- [x] **Array Size Asymmetry ($m > n$):**
  - Always guard with `if (nums1.size() > nums2.size()) return findMedianSortedArrays(nums2, nums1);`. This guarantees $m \le n$, which prevents $j = \text{half} - i$ from ever becoming negative or out-of-bounds.
- [x] **One Empty Array ($m = 0$):**
  - When $m = 0$, $i$ is immediately $0$. $\text{left1} = \text{INT\_MIN}$ and $\text{right1} = \text{INT\_MAX}$. The algorithm directly cuts `nums2` at $\text{half} = (n + 1) / 2$, yielding the correct median of `nums2`.
- [x] **Partition at Extreme Edges ($i = 0, i = m, j = 0, j = n$):**
  - Using `INT_MIN` for non-existent left elements and `INT_MAX` for non-existent right elements eliminates complex nested boundary branches.
- [x] **Odd vs. Even Parity:**
  - The unified formula `half = (m + n + 1) / 2` allocates the extra element to the left partition whenever $(m + n)$ is odd. Hence, for odd totals, the median is simply $\max(\text{left1}, \text{left2})$.
- [x] **Floating-Point Division:**
  - For even sums, dividing by `2.0` (double literal) avoids unintentional integer truncation.

---

## 5. Clean Code (Optimal Solution: Binary Search on Partition)

```cpp
#include <vector>
#include <algorithm>
#include <climits>

using namespace std;

class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        // Always binary search on the smaller array.
        if (nums1.size() > nums2.size()) {
            return findMedianSortedArrays(nums2, nums1);
        }

        int m = nums1.size();
        int n = nums2.size();

        // Number of elements that must be on the left side of the partition.
        int half = (m + n + 1) / 2;

        int left = max(0, half - n);
        int right = min(half, m);

        while (left <= right) {
            int i = left;
            int j = half - i;

            int left1 = (i == 0) ? INT_MIN : nums1[i - 1];
            int right1 = (i == m) ? INT_MAX : nums1[i];

            int left2 = (j == 0) ? INT_MIN : nums2[j - 1];
            int right2 = (j == n) ? INT_MAX : nums2[j];

            // Partition is too far right in nums1.
            if (left1 > right2) {
                right = i - 1;
            }
            // Partition is too far left in nums1.
            else if (left2 > right1) {
                left = i + 1;
            }
            // Correct partition found.
            else {
                int maxLeft = max(left1, left2);

                if ((m + n) % 2 == 1) {
                    return maxLeft;
                }

                int minRight = min(right1, right2);
                return (maxLeft + minRight) / 2.0;
            }
        }

        return 0.0;
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

#### Example 1: `nums1 = [1, 3]`, `nums2 = [2]`
- $m = 2, n = 1 \implies \text{Swap!}$ Now `nums1 = [2]`, `nums2 = [1, 3]`.
- $m = 1, n = 2 \implies \text{half} = (1 + 2 + 1) / 2 = 2$.
- Search range: `left = max(0, 2 - 2) = 0`, `right = min(2, 1) = 1`.

```text
Iteration 1:
  left = 0, right = 1
  i = 0, j = 2 - 0 = 2
  left1 = INT_MIN, right1 = nums1[0] = 2
  left2 = nums2[1] = 3, right2 = INT_MAX
  Check:
    left2 > right1 (3 > 2) -> Partition in nums1 is too far left!
    -> left = i + 1 = 1

Iteration 2:
  left = 1, right = 1
  i = 1, j = 2 - 1 = 1
  left1 = nums1[0] = 2, right1 = INT_MAX
  left2 = nums2[0] = 1, right2 = nums2[1] = 3
  Check:
    left1 <= right2 (2 <= 3) -> TRUE
    left2 <= right1 (1 <= INT_MAX) -> TRUE
  Partition is valid!
  Total length (1 + 2 = 3) is odd.
  Return maxLeft = max(left1, left2) = max(2, 1) = 2.0.
```

---

### The Architectural Pattern

```text
                    Partition Cut Invariant

      nums1:  [ ... left1 ]  |  [ right1 ... ]
                             |
      nums2:  [ ... left2 ]  |  [ right2 ... ]
              <───────────>     <────────────>
                Left Half          Right Half
             (half elements)

Condition for Balanced Median:
  left1 <= right2  AND  left2 <= right1

Adjustment Rules:
  left1 > right2  ──>  Cut too far right in nums1  ──>  right = i - 1
  left2 > right1  ──>  Cut too far left in nums1   ──>  left  = i + 1
```

* **Next Review Date:** Low priority (benchmark partition binary search mastered).
* **Key Takeaway:** Never merge sorted arrays to find the median; partition both arrays concurrently such that `left1 <= right2` and `left2 <= right1`. By binary searching exclusively on the cut point $i$ of the smaller array, the search space collapses in $O(\log(\min(m, n)))$ time with $O(1)$ space.
