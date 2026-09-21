# 0003. Longest Substring Without Repeating Characters

- **Problem Link:** https://leetcode.com/problems/longest-substring-without-repeating-characters/
- **Difficulty:** `Medium`
- **Topic / Pattern:** `Sliding Window` / `Hash Table` / `String`
- **Last Practiced:** 2026-09-21
- **Proficiency Level:** 
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:** *"Given a string `s`, find the length of the longest substring without repeating characters"*, *"substring"* (must be contiguous), $s.\text{length} \le 10^5$, containing letters, digits, symbols, and spaces.
- **Core intuition:**
  - A substring is defined by a contiguous window $[left \dots right]$.
  - The window must maintain the invariant: **zero duplicate characters**.
  - Instead of shrinking `left` one step at a time when a duplicate is hit (via an `unordered_set` and `while` loop), we can record the **last seen index** of every character: `lastSeen[c]`.
  - When character $c = s[right]$ is encountered:
    - If $c$ has already been seen inside the current window ($lastSeen[c] \ge left$), we immediately **jump** $left$ to $lastSeen[c] + 1$.
    - This eliminates all characters up to the duplicate in a single $O(1)$ leap.
    - We update $lastSeen[c] = right$ and compute the window width: $right - left + 1$.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Brute Force ($O(N^3)$ / $O(N^2)$ Time, $O(\min(N, \Sigma))$ Space):**
   - Check all $O(N^2)$ possible substrings and verify uniqueness using a hash set in $O(N)$ or $O(1)$.
   - *Verdict:* With $N = 10^5$, $N^2 = 10^{10} \rightarrow$ Time Limit Exceeded (TLE).

2. **Approach 2 — Sliding Window with `unordered_set` ($O(N)$ Time, $O(\Sigma)$ Space):**
   - Maintain a window $[left, right]$ and insert elements into `unordered_set<char>`.
   - When encountering a duplicate $s[right]$, run a `while` loop to delete characters from the left:
     ```cpp
     while (seen.count(s[right])) {
         seen.erase(s[left++]);
     }
     ```
   - *Verdict:* Valid $O(N)$ average time, but requires incremental character-by-character deletion and incurs `std::unordered_set` hashing / bucket overhead.

3. **Approach 3 — Sliding Window + Last Seen Index + Fixed Array (Optimal & Implemented):**
   - Maintain `array<int, 128> lastSeen` initialized to `-1`.
   - Expand `right` across the string:
     - If $lastSeen[c] \ge left$: Jump $left = lastSeen[c] + 1$.
     - Record $lastSeen[c] = right$.
     - Update $maxLength = \max(maxLength, right - left + 1)$.
   - *Verdict:* Optimal $O(N)$ time, $O(1)$ space. Zero dynamic memory allocation, cache-friendly array indexing, instant $O(1)$ window jumps.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$
  - The `right` pointer iterates through the string of length $N$ exactly once.
  - The `left` pointer only jumps strictly forward (never steps backward).
  - Every table lookup and update is $O(1)$ direct array indexing.
- **Space Complexity:** $O(1)$
  - Uses `std::array<int, 128>` which takes exactly $128 \times 4 = 512$ bytes on the stack, regardless of the input string length $N$.

---

## 4. Edge Cases & Gotchas

- [x] **The Backward-Jump Bug (`lastSeen[c] >= left` is mandatory):**
  - **Why not simply `left = lastSeen[c] + 1`?**
  - Consider $s = \text{"abba"}$:
    1. After processing `"abb"`: $left = 2$ (the window is `[b]`).
    2. At index 3, we encounter `'a'`. The character `'a'` was last seen at index 0.
    3. Notice that index 0 is **outside** the active window ($0 < 2$)!
    4. If you assign $left = lastSeen[\text{'a'}] + 1 = 0 + 1 = 1$, the left pointer would regress backwards from 2 to 1, re-introducing the duplicate `'b'` into the window!
  - **Rule:** Only advance `left` if the previous occurrence of $c$ lies **inside or at the boundary of the active window** ($lastSeen[c] \ge left$).
- [x] **Empty string ($s = \text{""}$):** The loop does not execute; returns $maxLength = 0$.
- [x] **Single character ($s = \text{"a"}$):** Window size is $0 - 0 + 1 = 1$; returns 1.
- [x] **All duplicate characters ($s = \text{"bbbbb"}$):** Window jumps at every step, maintaining length 1; returns 1.
- [x] **All unique characters ($s = \text{"abcdef"}$):** $left$ stays at 0 throughout; returns 6.
- [x] **Symbols, digits, and spaces ($s = \text{"abc def!@#abc"}$):** Fully covered by ASCII table $[0, 127]$ using `unsigned char` casting.

---

## 5. Clean Code (Optimal Solution: Sliding Window + Last Seen Index)

```cpp
#include <string>
#include <array>
#include <algorithm>

using namespace std;

class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        // Table of last seen indices for ASCII characters (0 - 127)
        array<int, 128> lastSeen;
        lastSeen.fill(-1);

        int left = 0;
        int maxLength = 0;

        for (int right = 0; right < s.size(); ++right) {
            unsigned char c = static_cast<unsigned char>(s[right]);

            // If c was previously seen within the current window, jump left past it
            if (lastSeen[c] >= left) {
                left = lastSeen[c] + 1;
            }

            // Record the newest position of character c
            lastSeen[c] = right;

            // Expand or maintain the maximum valid window length
            maxLength = max(maxLength, right - left + 1);
        }

        return maxLength;
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

#### Case 1: `s = "abcabcbb"`

```text
Initial state: left = 0, maxLength = 0, lastSeen = all -1

right = 0 ('a'): lastSeen['a'] = -1 < 0 -> left = 0, lastSeen['a'] = 0, maxLen = 1  Window: [a]
right = 1 ('b'): lastSeen['b'] = -1 < 0 -> left = 0, lastSeen['b'] = 1, maxLen = 2  Window: [ab]
right = 2 ('c'): lastSeen['c'] = -1 < 0 -> left = 0, lastSeen['c'] = 2, maxLen = 3  Window: [abc]
right = 3 ('a'): lastSeen['a'] = 0 >= 0 -> left = 0 + 1 = 1, lastSeen['a'] = 3, maxLen = 3 Window: [bca]
right = 4 ('b'): lastSeen['b'] = 1 >= 1 -> left = 1 + 1 = 2, lastSeen['b'] = 4, maxLen = 3 Window: [cab]
right = 5 ('c'): lastSeen['c'] = 2 >= 2 -> left = 2 + 1 = 3, lastSeen['c'] = 5, maxLen = 3 Window: [abc]
right = 6 ('b'): lastSeen['b'] = 4 >= 3 -> left = 4 + 1 = 5, lastSeen['b'] = 6, maxLen = 3 Window: [cb]
right = 7 ('b'): lastSeen['b'] = 6 >= 5 -> left = 6 + 1 = 7, lastSeen['b'] = 7, maxLen = 3 Window: [b]

Result: 3 ("abc")
```

#### Case 2: `s = "abba"` (The Backward Jump Hazard)

```text
right = 0 ('a'): lastSeen['a'] = 0, left = 0, maxLen = 1   Window: [a]
right = 1 ('b'): lastSeen['b'] = 1, left = 0, maxLen = 2   Window: [ab]
right = 2 ('b'): lastSeen['b'] = 1 >= 0 -> left = 1 + 1 = 2, lastSeen['b'] = 2, maxLen = 2 Window: [b]
right = 3 ('a'): lastSeen['a'] = 0.
                 Check: is lastSeen['a'] >= left? (0 >= 2 is FALSE!)
                 -> Do NOT move left backwards! left remains 2.
                 lastSeen['a'] = 3, maxLen = max(2, 3 - 2 + 1) = 2  Window: [ba]

Result: 2 ("ab" or "ba")
```

---

### Why `array<int, 128>` Over `unordered_map<char, int>`?

In competitive programming and high-performance C++:
- `unordered_map`: Involves hash calculations, linked lists / buckets, dynamic heap allocations, and higher memory footprint per entry.
- `array<int, 128>`: Contiguous stack allocation of 512 bytes, L1 cache friendly, direct index offset calculation $O(1)$ with near-zero constant overhead.

---

### Comparison: Set Approach vs. Last Seen Approach

```text
Set Approach:
  Duplicate hit -> while loop -> remove characters one-by-one from left -> move left

Last Seen Approach:
  Duplicate hit -> jump left directly to lastSeen[c] + 1 (if in window)
```

---

### The Architectural Pattern

```text
Longest Substring Without Repeating Characters
                     ↓
               Sliding Window
                     ↓
            lastSeen[c] = -1
                     ↓
          for right in 0 .. n - 1:
                     ├─ if lastSeen[c] >= left:
                     │       left = lastSeen[c] + 1  (jump left!)
                     ├─ lastSeen[c] = right
                     └─ maxLength = max(maxLength, right - left + 1)
                     ↓
              return maxLength
```

* **Next Review Date:** Low priority (benchmark variable-size sliding window with index jumping mastered).
* **Key Takeaway:** For substrings with uniqueness constraints, tracking the *last seen index* enables $O(1)$ direct left pointer jumps. Always guard with `lastSeen[c] >= left` to prevent the window from ever moving backwards.

