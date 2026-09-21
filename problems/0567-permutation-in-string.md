# 0567. Permutation in String

- **Problem Link:** https://leetcode.com/problems/permutation-in-string/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Sliding Window`
- **LeetCode Topics:** `Hash Table` / `Two Pointers` / `String` / `Sliding Window`
- **Core Pattern:** `Fixed Sliding Window + Frequency Array Equality`
- **Last Practiced:** 2026-09-21
- **Proficiency Level:** 
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:** *"Given two strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1`, or `false` otherwise"*, *"in other words, return `true` if one of `s1`'s permutations is the substring of `s2`"*, lowercase English letters only, lengths up to $10^4$.
- **Core intuition:**
  - A **permutation** of a string is simply a rearrangement of its characters. Two strings are permutations of each other if and only if they possess **identical character frequencies** across all 26 letters.
  - Generating all permutations is impossible: $|s_1|!$ explodes exponentially ($O(K!)$).
  - Sorting every candidate substring costs $O((N - K + 1) \cdot K \log K)$, which is far too slow.
  - Crucial insight: Every permutation of $s_1$ must have length **strictly equal** to $|s_1|$.
  - Therefore, this problem reduces to finding a **fixed-size window** of length $K = |s_1|$ inside $s_2$ whose character frequency signature matches that of $s_1$.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Generate All Permutations ($O(K! \cdot N)$ Time, $O(K!)$ Space):**
   - Generate all permutations of $s_1$ and search for each in $s_2$.
   - *Verdict:* $K!$ is astronomical even for $K = 15$ ($15! \approx 1.3 \times 10^{12}$) $\rightarrow$ Memory Limit Exceeded / TLE.

2. **Approach 2 — Sort-Based Window Search ($O(N \cdot K \log K)$ Time, $O(K)$ Space):**
   - For every window of size $K$ in $s_2$, create a copy, sort it, and compare with `sorted(s1)`.
   - *Verdict:* Sorting takes $O(K \log K)$ at every step. Inefficient for $K \le 10^4$.

3. **Approach 3 — Fixed Sliding Window + Frequency Array (Optimal & Implemented):**
   - Precompute `array<int, 26> need` counting the frequencies of characters in $s_1$.
   - Slide a window of fixed width $K = |s_1|$ through $s_2$ using `array<int, 26> window`:
     - Add incoming character: `++window[s2[right] - 'a']`.
     - When $right \ge K$: remove the outgoing character that falls out of the window: `--window[s2[right - K] - 'a']`.
     - Compare: `if (window == need) return true;`.
   - *Verdict:* Optimal $O(N)$ time, $O(1)$ space. `std::array::operator==` performs an unrolled, vectorized 26-integer comparison taking mere nanoseconds.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$ where $N = |s_2|$ and $K = |s_1|$
  - Counting frequencies of $s_1$: $O(K)$ steps.
  - Iterating through $s_2$: $N$ iterations. In each iteration:
    - Incrementing and decrementing array counts: $O(1)$.
    - Comparing `window == need`: checks 26 fixed integers ($O(26) = O(1)$).
    - Total operations: $\approx 26 \times 10^4 = 2.6 \times 10^5$, executing in $< 2\text{ms}$.
- **Space Complexity:** $O(1)$
  - Uses two fixed `std::array<int, 26>` on the stack ($2 \times 26 \times 4 = 208$ bytes total), independent of string lengths.

---

## 4. Edge Cases & Gotchas

- [x] **$|s_1| > |s_2|$:** A longer string can never be a substring of a shorter string. Return `false` immediately at the very beginning (`if (s1.size() > s2.size()) return false;`).
- [x] **Permutation at the very beginning of $s_2$:** The first window $[0 \dots K - 1]$ matches `need`; correctly triggers `window == need` at $right = K - 1$ and returns `true`.
- [x] **Permutation at the very end of $s_2$:** Handled cleanly as the loop completes at $right = N - 1$.
- [x] **$|s_1| = 1$:** Window size is 1. The window shrinks and shifts by 1 character each step, behaving like a single character search.
- [x] **All identical characters (e.g. $s_1 = \text{"aaa"}$, $s_2 = \text{"aaaa"}$):** Correctly tracks counts and returns `true`.
- [x] **Why compare arrays (`window == need`) instead of tracking a `matches` counter?**
  - Tracking an integer `matches` (counting how many of the 26 characters have identical counts) reduces the comparison from 26 operations to 1.
  - However, for $|\Sigma| = 26$, 26 integer comparisons are trivially cheap and vectorized by modern compilers. The `window == need` approach is infinitely cleaner, less error-prone, and 100% bug-free for interview conditions.

---

## 5. Clean Code (Optimal Solution: Fixed Sliding Window + Frequency Array)

```cpp
#include <string>
#include <array>

using namespace std;

class Solution {
public:
    bool checkInclusion(string s1, string s2) {
        // Base case: s1 cannot be a substring of s2 if it is longer
        if (s1.size() > s2.size()) {
            return false;
        }

        array<int, 26> need{};
        array<int, 26> window{};

        // Record target character frequencies of s1
        for (char c : s1) {
            ++need[c - 'a'];
        }

        int windowSize = s1.size();

        for (int right = 0; right < s2.size(); ++right) {
            // Include current character into the sliding window
            ++window[s2[right] - 'a'];

            // Maintain fixed window size by evicting the leftmost character
            if (right >= windowSize) {
                --window[s2[right - windowSize] - 'a'];
            }

            // Check if current window matches the required frequency signature
            if (window == need) {
                return true;
            }
        }

        return false;
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given `s1 = "ab"`, `s2 = "eidbaooo"`:

```text
Window size K = 2
Target need: {'a': 1, 'b': 1}

right = 0 ('e'): window: {'e': 1}                             right < 2 -> no eviction -> window != need
right = 1 ('i'): window: {'e': 1, 'i': 1}                     right < 2 -> no eviction -> window != need  (Window: "ei")
right = 2 ('d'): window: {'e': 1, 'i': 1, 'd': 1}
                 right >= 2 -> evict s2[0]='e':
                 window: {'i': 1, 'd': 1}                     window != need (Window: "id")
right = 3 ('b'): window: {'i': 1, 'd': 1, 'b': 1}
                 right >= 2 -> evict s2[1]='i':
                 window: {'d': 1, 'b': 1}                     window != need (Window: "db")
right = 4 ('a'): window: {'d': 1, 'b': 1, 'a': 1}
                 right >= 2 -> evict s2[2]='d':
                 window: {'b': 1, 'a': 1}                     window == need -> MATCH FOUND!
                 Return: true ("ba" is a permutation of "ab")
```

---

### Variable vs. Fixed Sliding Window

| Problem | Window Type | Size Condition | Movement Strategy |
| :--- | :--- | :--- | :--- |
| **0003. Longest Substring Without Repeating** | Variable | Dynamic ($0 \dots N$) | Expand `right`, jump `left = lastSeen[c] + 1` on duplicate |
| **0424. Longest Repeating Replacement** | Variable | Dynamic ($0 \dots N$) | Expand `right`, shrink `left++` while `winSize - maxFreq > k` |
| **0567. Permutation in String** | **Fixed** | **Constant** ($|s_1|$) | Expand `right`, evict `left = right - K` when `right >= K` |

---

### The Architectural Pattern

```text
Permutation in String
          ↓
     s1.size() > s2.size()? ── Yes ──> return false
          ↓ No
   need = count(s1)
   K = s1.size()
          ↓
  for right in 0 .. s2.size() - 1:
          ├─ ++window[s2[right] - 'a']
          ├─ if right >= K:
          │       --window[s2[right - K] - 'a']  (evict leftmost)
          ├─ if window == need:
          │       return true                     (permutation match!)
          ↓
    return false
```

* **Next Review Date:** Low priority (benchmark fixed-size frequency sliding window mastered).
* **Key Takeaway:** Any problem inquiring whether a permutation exists inside a text is a **fixed-size sliding window** problem. Maintain the window length strictly equal to $|s_1|$ and verify signature parity using fixed-size frequency tables.
