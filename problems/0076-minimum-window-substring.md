# 0076. Minimum Window Substring

- **Problem Link:** https://leetcode.com/problems/minimum-window-substring/
- **Difficulty:** `Hard`
- **NeetCode Category:** `Sliding Window`
- **LeetCode Topics:** `Hash Table` / `String` / `Sliding Window`
- **Core Pattern:** `Variable Sliding Window + Frequency Array + formed/required Count`
- **Last Practiced:** 2026-09-22
- **Proficiency Level:** 
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:** *"Given two strings `s` and `t` of lengths `m` and `n` respectively"*, *"return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window"*, *"if there is no such substring, return the empty string `\"\"`"*, constraints up to $10^5$.
- **Core intuition:**
  - This is the benchmark **variable-size sliding window (shrink to minimize)** problem.
  - The window $[left \dots right]$ expands to the right until it becomes **valid** (contains all characters of $t$ with sufficient frequencies).
  - Once the window is valid, it attempts to **shrink from the left** ($left++$) as much as possible to minimize the window length, recording the minimal length along the way, until it just becomes invalid.
  - Repeating this process across string $s$ yields the globally minimal valid window in $O(m + n)$ time.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Brute Force ($O(m^2 \cdot n)$ Time, $O(1)$ Space):**
   - Check all $O(m^2)$ substrings of $s$. For each substring, count character frequencies and verify if it covers all characters in $t$.
   - *Verdict:* With $m = 10^5$, $m^2 = 10^{10} \rightarrow$ Time Limit Exceeded (TLE).

2. **Approach 2 — Sliding Window + `unordered_map` with Type-Count Matches ($O(m + n)$ Time, $O(|\Sigma|)$ Space):**
   - Track counts using `unordered_map<char, int>`.
   - Count matching *unique character types* (e.g. `formed == required_unique_chars`).
   - *Verdict:* Valid and optimal asymptotic complexity, but `unordered_map` introduces heap allocation, bucket traversal, and hash overhead.

3. **Approach 3 — Sliding Window + Frequency Arrays + Character Count `formed` (Optimal & Implemented):**
   - Use two fixed arrays `array<int, 128> need{}` and `array<int, 128> window{}`.
   - Define `required = t.size()` (total character occurrences needed, accounting for duplicates).
   - Track `formed` = total valid character occurrences matched inside the window:
     - Expand `right`: `++window[c]`. If `window[c] <= need[c]`, increment `++formed`.
     - While `formed == required` (window is valid):
       - Record best window: `[bestStart, bestLength]`.
       - Evict `leftChar = s[left]`: `--window[leftChar]`.
       - If `window[leftChar] < need[leftChar]`, decrement `--formed`.
       - Advance `++left`.
   - *Verdict:* Optimal $O(m + n)$ time, $O(1)$ space. Zero heap allocations, direct cache-friendly array lookups, and clear symmetrical `formed` update logic.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(m + n)$
  - Precomputing `need` from $t$: $O(n)$ steps.
  - Sliding window across $s$:
    - The `right` pointer advances from $0$ to $m - 1$ ($m$ steps).
    - The `left` pointer only advances forward from $0$ to $m$ ($m$ steps at most across the entire execution).
    - Each character entry and exit performs $O(1)$ array lookups and arithmetic operations.
  - Overall time: $O(m + n)$.
- **Space Complexity:** $O(1)$
  - Two fixed arrays of size 128 on the stack: $2 \times 128 \times 4 = 1024$ bytes ($1\text{ KB}$), independent of $m$ and $n$.

---

## 4. Edge Cases & Gotchas

- [x] **$|t| > |s|$:** A window cannot exist if $t$ has more characters than $s$. Return `""` immediately (`if (t.size() > s.size()) return "";`).
- [x] **Counting Occurrences vs. Types (`required = t.size()`):**
  - Tracking by total character count `t.size()` is clean and handles duplicate characters in $t$ naturally.
  - Example: $t = \text{"AABC"}$. Here `need['A'] = 2, need['B'] = 1, need['C'] = 1`, and `required = 4`.
  - When the window encounters three `'A'`s:
    - 1st `'A'`: `window['A'] = 1 <= 2` $\rightarrow$ `++formed` (1/4).
    - 2nd `'A'`: `window['A'] = 2 <= 2` $\rightarrow$ `++formed` (2/4).
    - 3rd `'A'`: `window['A'] = 3 > 2` $\rightarrow$ **does NOT increment `formed`!**
    - The 3rd `'A'` is redundant for satisfying $t$.
- [x] **Symmetrical Eviction Condition:**
  - Evicting from left: `--window[leftChar]`.
  - If `window[leftChar] < need[leftChar]`: We just removed a **required** occurrence, so `formed` must decrement (`--formed`). If it was a surplus duplicate (e.g. going from 3 to 2 when `need` is 2), `formed` stays untouched.
- [x] **`while` vs `if` when `formed == required` (Crucial Pattern):**
  - When `formed == required`, the window is valid, but it may contain surplus characters on the left.
  - We must use a `while` loop to aggressively shrink from the left as long as the window remains valid, capturing the smallest possible span.
- [x] **No Valid Window Found:** If `bestLength` remains `INT_MAX`, return `""`.
- [x] **Single Character Match ($s = \text{"a"}, t = \text{"a"}$):** Correctly finds window `"a"`.

---

## 5. Clean Code (Optimal Solution: Sliding Window + Frequency Array + formed Count)

```cpp
#include <string>
#include <array>
#include <climits>

using namespace std;

class Solution {
public:
    string minWindow(string s, string t) {
        if (t.size() > s.size()) {
            return "";
        }

        array<int, 128> need{};
        array<int, 128> window{};

        // Frequency required for each character in t
        for (char c : t) {
            ++need[static_cast<unsigned char>(c)];
        }

        int required = static_cast<int>(t.size());
        int formed = 0;

        int left = 0;
        int bestStart = 0;
        int bestLength = INT_MAX;

        for (int right = 0; right < s.size(); ++right) {
            unsigned char c = static_cast<unsigned char>(s[right]);
            ++window[c];

            // This character contributes towards satisfying t
            // only while its window count does not exceed the required need
            if (window[c] <= need[c]) {
                ++formed;
            }

            // Current window contains all characters required by t:
            // Shrink from the left to find the minimal valid window
            while (formed == required) {
                int length = right - left + 1;
                if (length < bestLength) {
                    bestLength = length;
                    bestStart = left;
                }

                unsigned char leftChar = static_cast<unsigned char>(s[left]);
                --window[leftChar];

                // Removing this character breaks validity only if
                // its count drops strictly below what t requires
                if (window[leftChar] < need[leftChar]) {
                    --formed;
                }

                ++left;
            }
        }

        return bestLength == INT_MAX ? "" : s.substr(bestStart, bestLength);
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given `s = "ADOBECODEBANC"`, `t = "ABC"`:

```text
need: {'A': 1, 'B': 1, 'C': 1}, required = 3

right = 0 ('A'): window['A']=1 <= 1 -> formed = 1. Window: "A"
right = 1 ('D'): window['D']=1 > 0  -> formed = 1. Window: "AD"
right = 2 ('O'): window['O']=1 > 0  -> formed = 1. Window: "ADO"
right = 3 ('B'): window['B']=1 <= 1 -> formed = 2. Window: "ADOB"
right = 4 ('E'): window['E']=1 > 0  -> formed = 2. Window: "ADOBE"
right = 5 ('C'): window['C']=1 <= 1 -> formed = 3 == required!
                 Window "ADOBEC" (length 6) is VALID.
                 Record: bestLength = 6, bestStart = 0 ("ADOBEC").
                 Shrink left:
                   left = 0 ('A'): window['A'] becomes 0 < 1 -> formed = 2 < 3. left = 1.
                 Stop shrink.

right = 6..9: expands through "ODEB"
right = 10 ('A'): window now contains 'B' (index 9), 'C' (index 5), 'A' (index 10).
                  formed == 3! Window: "DOBECODEBA"
                  Shrink left aggressively:
                    remove 'D', 'O', 'B', 'E', 'C', 'O', 'D', 'E'...
right = 12 ('C'): window reaches end with "BANC".
                  formed == 3! Window: "BANC" (length 4).
                  bestLength = 4, bestStart = 9 ("BANC").

Final Result: "BANC"
```

---

### Sliding Window Taxonomy in NeetCode 150

| Problem | Window Type | Invariant / Condition | Goal |
| :--- | :--- | :--- | :--- |
| **0003. Longest Substring Without Repeating** | Variable | Window must have zero duplicates | Maximize window size |
| **0424. Longest Repeating Replacement** | Variable | $\text{winSize} - maxFreq \le k$ | Maximize window size |
| **0567. Permutation in String** | Fixed | $\text{winSize} == |s_1|$ strictly | Find any exact match |
| **0076. Minimum Window Substring** | Variable | Window must cover all characters of $t$ | **Minimize window size** |

---

### The Architectural Pattern

```text
Minimum Window Substring
           ↓
     t.size() > s.size()? ── Yes ──> return ""
           ↓ No
   need = count(t)
   required = t.size()
           ↓
  for right in 0 .. s.size() - 1:
           ├─ ++window[s[right]]
           ├─ if window[s[right]] <= need[s[right]]:
           │       ++formed
           ├─ while formed == required:
           │       update [bestStart, bestLength]
           │       --window[s[left]]
           │       if window[s[left]] < need[s[left]]:
           │             --formed
           │       ++left
           ↓
  return bestLength == INT_MAX ? "" : s.substr(bestStart, bestLength)
```

* **Next Review Date:** Low priority (benchmark variable-size shrinking sliding window mastered).
* **Key Takeaway:** For minimum window problems, expand `right` until valid, then greedily shrink `left` with a `while` loop while validity holds. Tracking total occurrences via `formed == required` ensures clean and symmetric duplicate handling.

