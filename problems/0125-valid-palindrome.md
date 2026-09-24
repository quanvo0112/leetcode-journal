# 0125. Valid Palindrome

- **Problem Link:** https://leetcode.com/problems/valid-palindrome/
- **Difficulty:** `Easy`
- **NeetCode Category:** `Two Pointers`
- **LeetCode Topics:** `Two Pointers` / `String`
- **Core Pattern:** `In-place Two Pointers (isalnum / tolower Filtering)`
- **Last Practiced:** 2026-09-19
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers
- Clues in prompt: *"reads the same forward and backward"*, *"after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters"*.
- Core intuition: A palindrome has mirror symmetry across its center. Rather than filtering out invalid characters into a new string and reversing it (which costs $O(N)$ auxiliary memory), we can validate mirror symmetry in-place using **Two Pointers** (`left` moving rightward, `right` moving leftward). Each pointer skips non-alphanumeric characters on the fly and compares the normalized characters until the pointers meet in the middle.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Filter & Reverse ($O(N)$ Time, $O(N)$ Space):**
   - Iterate through the string, filter valid alphanumeric characters into a new string `t`, and check `t == string(t.rbegin(), t.rend())`.
   - *Verdict:* Intuitive and easy to write, but wastes $O(N)$ auxiliary memory by allocating new heap strings and buffer copies.

2. **Approach 2 — Two Pointers In-Place (Optimal & Implemented):**
   - Initialize `left = 0` and `right = s.size() - 1`.
   - While `left < right`:
     - Advance `left` until `s[left]` is alphanumeric.
     - Decrement `right` until `s[right]` is alphanumeric.
     - Compare `tolower(s[left]) != tolower(s[right])`. If mismatched, return `false` immediately (early termination).
     - Narrow the window: `++left; --right;`.
   - *Verdict:* Strictly $O(1)$ auxiliary space and $O(N)$ time. Single pass over the original string buffer with zero dynamic allocations.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$
  - Each character in the string is visited at most a constant number of times (by either the outer pointer movement or inner skip loops).
  - The pointers `left` and `right` traverse towards each other and terminate once they meet or cross in $\le N$ total steps.
- **Space Complexity:** $O(1)$
  - Only two scalar integer pointer variables (`left`, `right`) on the stack. No string copies or dynamic memory allocation.

---

## 4. Edge Cases & Gotchas
- [x] **Empty string or string with only whitespace/punctuation (e.g. `s = "   "` or `s = ".,"`):** The inner `while` loops safely advance until `left >= right`, at which point the outer loop exits cleanly and returns `true`.
- [x] **Single alphanumeric character (e.g. `s = "a"`):** Pointers satisfy `left == right` immediately; loop does not execute and correctly returns `true`.
- [x] **C++ `<cctype>` undefined behavior pitfall:** Functions like `isalnum()` and `tolower()` take an `int` argument, which must be representable as an `unsigned char` or equal to `EOF`. Passing a raw signed `char` with a negative value (e.g. characters in extended ASCII $\ge 128$) causes **Undefined Behavior**. Always cast explicitly: `static_cast<unsigned char>(s[i])`.

---

## 5. Clean Code (Optimal Solution: In-Place Two Pointers)

```cpp
class Solution {
public:
    bool isPalindrome(string s) {
        int left = 0;
        int right = static_cast<int>(s.size()) - 1;

        while (left < right) {
            // Skip non-alphanumeric characters from the left
            while (left < right && !isalnum(static_cast<unsigned char>(s[left]))) {
                ++left;
            }

            // Skip non-alphanumeric characters from the right
            while (left < right && !isalnum(static_cast<unsigned char>(s[right]))) {
                --right;
            }

            // Compare normalized lowercase characters
            if (tolower(static_cast<unsigned char>(s[left])) !=
                tolower(static_cast<unsigned char>(s[right]))) {
                return false;
            }

            ++left;
            --right;
        }

        return true;
    }
};
```

---

## 6. Review & Takeaways

### Visualizing Two Pointers Convergence

Given `s = " A man, a plan, a canal: Panama "`:

```text
Step 1:
left  →                                   ← right
"   A   m a n ,   a   p l a n . . . P a n a m a   "
    ↑                                       ↑
(skip spaces/punctuation until both point to letters)

Step 2:
left points to 'A', right points to 'a'
tolower('A') == tolower('a') -> Match!
++left; --right;

... (inward convergence continues) ...

Result: All characters match symmetrically -> returns true.
```

---

### C++ Senior Interview Deep Dive: Why `static_cast<unsigned char>`?

The ISO C++ standard specifies that functions in `<cctype>` (`isalnum`, `isalpha`, `tolower`, etc.) are inherited from the C standard library. Their signatures are:

```cpp
int isalnum(int ch);
int tolower(int ch);
```

The standard mandates that the value of `ch` **must be representable as an `unsigned char` or equal to `EOF`**.

On platforms where `char` is signed (the default on most x86/ARM compilers), any non-ASCII byte with the high bit set has a negative value when widened to `int`. Passing a negative value other than `EOF` results in an **out-of-bounds lookup into the internal character-classification table** (Undefined Behavior / memory fault).

```cpp
// UNSAFE: Can trigger undefined behavior on signed char systems:
isalnum(s[left]);

// SAFE & ROBUST: Standards-compliant across all architectures:
isalnum(static_cast<unsigned char>(s[left]));
```

Writing this demonstrates deep systems-level awareness and standard library fluency in technical interviews.

---

### The Core Architectural Pattern

```text
Valid Palindrome
       ↓
Two Pointers (left = 0, right = n - 1)
       ↓
Skip invalid characters (while !isalnum)
       ↓
Compare normalized characters (tolower)
       ↓
Move inward (++left, --right)
```

* **Next Review Date:** Low priority (benchmark two pointers symmetry pattern mastered).
* **Key Takeaway:** For sequence symmetry or pair verification without auxiliary space, use converging two pointers traversing directly on the input buffer.
