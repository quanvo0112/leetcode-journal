# 0424. Longest Repeating Character Replacement

- **Problem Link:** https://leetcode.com/problems/longest-repeating-character-replacement/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Sliding Window`
- **LeetCode Topics:** `Hash Table` / `String` / `Sliding Window`
- **Core Pattern:** `Variable Sliding Window + Frequency Array + maxFreq`
- **Last Practiced:** 2026-09-21
- **Proficiency Level:** 
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:** *"Given a string `s` and an integer `k`"*, *"choose any character of the string and change it to any other uppercase English character at most `k` times"*, *"return the length of the longest substring containing the same letter you can get after performing the above operations"*.
- **Core intuition:**
  - A valid substring has all its characters identical after at most $k$ replacements.
  - For any contiguous window $[left \dots right]$:
    - To minimize the number of replacements, we should always preserve the character that appears **most frequently** in this window, and change all other characters to match it.
    - Let $maxFreq$ be the highest frequency of any single character currently in the window.
    - Then the number of replacement operations required is:
      $$\text{replacements} = \text{windowSize} - maxFreq = (right - left + 1) - maxFreq$$
    - If $\text{replacements} \le k$: The current window is **valid** (can be transformed into all identical letters).
    - If $\text{replacements} > k$: The current window is **invalid** (requires more than $k$ replacements). We must shrink from the left ($left++$).

---

## 2. Approach & Trade-offs

1. **Approach 1 — Brute Force ($O(N^2)$ Time, $O(26) = O(1)$ Space):**
   - Check all $O(N^2)$ substrings. For each substring, count character frequencies to find the majority character and determine whether $\text{length} - maxFreq \le k$.
   - *Verdict:* With $N = 10^5$, $N^2 = 10^{10} \rightarrow$ Time Limit Exceeded (TLE).

2. **Approach 2 — Sliding Window + Full Frequency Scan on Shrink ($O(26 \cdot N) \approx O(N)$ Time):**
   - Whenever the window shrinks, re-scan the 26 frequency counts to compute the exact new $maxFreq$.
   - *Verdict:* Valid and optimal asymptotic time, but re-scanning 26 elements during every shrinkage adds unnecessary constant overhead.

3. **Approach 3 — Sliding Window + Frequency Array + Running `maxFreq` (Optimal & Implemented):**
   - Use `array<int, 26> freq{}` to track character counts in the current window.
   - Maintain a running scalar $maxFreq$.
   - As $right$ expands:
     - Increment `freq[s[right] - 'A']`.
     - Update $maxFreq = \max(maxFreq, freq[s[right] - 'A'])$.
     - While $(right - left + 1) - maxFreq > k$: decrement `freq[s[left] - 'A']` and advance $left++$.
     - Update $maxLength = \max(maxLength, right - left + 1)$.
   - *Verdict:* Optimal $O(N)$ time, $O(1)$ space. Zero heap allocation, minimal operations per character.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$
  - Each character is visited at most twice (once by $right$ when entering the window, and at most once by $left$ when leaving).
  - Inside the loop, all operations (array lookup, subtraction, comparison) take $O(1)$ constant time.
- **Space Complexity:** $O(1)$
  - A fixed `std::array<int, 26>` taking $26 \times 4 = 104$ bytes on the stack, completely independent of the input size $N$.

---

## 4. Edge Cases & Gotchas

- [x] **The Golden Formula (Avoid Inverting):**
  $$\text{replacements} = (right - left + 1) - maxFreq$$
  Do **not** invert the subtraction (e.g. $maxFreq - \text{windowSize}$). Replacements represent the "minority" characters in the window that need changing.
- [x] **Why `maxFreq` does not need to decrease during window shrinkage (Crucial Insight):**
  - When $left$ advances and `freq[s[left] - 'A']` decrements, the *actual* highest frequency inside the newly shrunken window might decrease.
  - However, we **do not need to decrement `maxFreq`**.
  - **Reason:** A smaller $maxFreq$ can never yield a new maximum window length that beats our best recorded $maxLength$. To establish a new maximum answer, we strictly require a window where a character achieves a frequency **strictly higher** than the historically recorded $maxFreq$.
  - Therefore, keeping $maxFreq$ as a historical high watermark is completely safe and avoids scanning the 26-element array on every shrinkage.
- [x] **$k$ is large ($k \ge N$):** The entire string can be converted to any single character; returns $N$.
- [x] **$k = 0$:** No replacements allowed; finds the longest contiguous run of identical characters.
- [x] **All characters identical ($s = \text{"AAAA"}$):** $\text{replacements} = 0 \le k$ always; returns $N$.
- [x] **Alternating characters ($s = \text{"ABAB"}$, $k = 1$):** Properly expands and shrinks to identify length 3 or 4.

---

## 5. Clean Code (Optimal Solution: Sliding Window + Frequency Array)

```cpp
#include <string>
#include <array>
#include <algorithm>

using namespace std;

class Solution {
public:
    int characterReplacement(string s, int k) {
        // Frequency array for uppercase English letters 'A' through 'Z'
        array<int, 26> freq{};
        
        int left = 0;
        int maxFreq = 0;
        int maxLength = 0;

        for (int right = 0; right < s.size(); ++right) {
            int index = s[right] - 'A';
            ++freq[index];
            maxFreq = max(maxFreq, freq[index]);

            // Number of characters in the window that must be replaced
            int replacements = (right - left + 1) - maxFreq;

            // If replacements exceed budget k, shrink the window from the left
            while (replacements > k) {
                --freq[s[left] - 'A'];
                ++left;
                replacements = (right - left + 1) - maxFreq;
            }

            // Record the largest valid window length found so far
            maxLength = max(maxLength, right - left + 1);
        }

        return maxLength;
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given `s = "AABABBA"`, `k = 1`:

```text
Initial state: left = 0, maxFreq = 0, maxLength = 0, freq = all 0

right = 0 ('A'): freq['A'] = 1, maxFreq = 1, winSize = 1, replacements = 1 - 1 = 0 <= 1 -> maxLen = 1  Window: [A]
right = 1 ('A'): freq['A'] = 2, maxFreq = 2, winSize = 2, replacements = 2 - 2 = 0 <= 1 -> maxLen = 2  Window: [AA]
right = 2 ('B'): freq['B'] = 1, maxFreq = 2, winSize = 3, replacements = 3 - 2 = 1 <= 1 -> maxLen = 3  Window: [AAB]
right = 3 ('A'): freq['A'] = 3, maxFreq = 3, winSize = 4, replacements = 4 - 3 = 1 <= 1 -> maxLen = 4  Window: [AABA] (Valid: replace 'B' -> 'A')
right = 4 ('B'): freq['B'] = 2, maxFreq = 3, winSize = 5, replacements = 5 - 3 = 2 > 1  -> INVALID!
                 Shrink: freq[s[0]='A'] becomes 2, left = 1.
                 New winSize = 5 - 1 = 4, replacements = 4 - 3 = 1 <= 1 -> valid!
                 maxLen = max(4, 4) = 4. Window: [ABAB]
right = 5 ('B'): freq['B'] = 3, maxFreq = 3, winSize = 6 - 1 = 5, replacements = 5 - 3 = 2 > 1 -> INVALID!
                 Shrink: freq[s[1]='A'] becomes 1, left = 2.
                 New winSize = 4, replacements = 4 - 3 = 1 <= 1 -> valid!
                 maxLen = max(4, 4) = 4. Window: [BABB]
right = 6 ('A'): freq['A'] = 2, maxFreq = 3, winSize = 7 - 2 = 5, replacements = 5 - 3 = 2 > 1 -> INVALID!
                 Shrink: freq[s[2]='B'] becomes 2, left = 3.
                 New winSize = 4, replacements = 4 - 3 = 1 <= 1 -> valid!
                 maxLen = max(4, 4) = 4. Window: [ABBA]

Final Result: 4 (e.g. "AABA" -> "AAAA" or "BABB" -> "BBBB")
```

---

### Why `array<int, 26>` Over `unordered_map<char, int>`?

- Since $s$ only contains uppercase English letters, direct indexing via `c - 'A'` maps contiguous slots $0 \dots 25$.
- Eliminates hash collisions, dynamic node allocations, and pointer dereferences.
- Entire frequency array easily fits into a single cache line (104 bytes $\le$ 2 cache lines of 64 bytes).

---

### The Architectural Pattern

```text
Longest Repeating Character Replacement
                   ↓
             Sliding Window
                   ↓
           freq[26] = {0}
                   ↓
         for right in 0 .. n - 1:
                   ├─ ++freq[s[right] - 'A']
                   ├─ maxFreq = max(maxFreq, freq[s[right] - 'A'])
                   ├─ while (right - left + 1) - maxFreq > k:
                   │       --freq[s[left] - 'A']
                   │       ++left
                   └─ maxLength = max(maxLength, right - left + 1)
                   ↓
            return maxLength
```

* **Next Review Date:** Low priority (benchmark variable-size sliding window with frequency bounds mastered).
* **Key Takeaway:** When allowed at most $k$ operations to make a window uniform, the number of changes required is always $\text{windowSize} - maxFreq$. Stale $maxFreq$ values during shrinking never invalidate the search for a new global maximum.

