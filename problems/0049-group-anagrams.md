# 0049. Group Anagrams

- **Problem Link:** https://leetcode.com/problems/group-anagrams/
- **Difficulty:** `Medium`
- **Topic / Pattern:** `Array` / `Hash Table` / `String` / `Counting`
- **Last Practiced:** 2026-09-18
- **Proficiency Level:** 
  - [x] 🟢 Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] 🟡 Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] 🔴 Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers
- Clues in prompt: *"group the anagrams together"*, *"lowercase English letters"*.
- Core intuition: Two strings are anagrams if and only if they possess identical character counts. To group them efficiently without sorting each word, map each string to an unambiguous **canonical frequency signature** that serves as the hash-map key.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Sorted String as Key:**
   - Sort each string alphabetically (`"eat"` $\rightarrow$ `"aet"`, `"tea"` $\rightarrow$ `"aet"`) and use the sorted string as the hash map key.
   - **Time:** $O(N \cdot K \log K)$, where $N$ is the number of strings and $K$ is the maximum length of a string.
   - **Space:** $O(N \cdot K)$ to store keys and grouped strings.
   - *Verdict:* Very concise code and easy to implement in interviews, but asymptotically slower for long strings.

2. **Approach 2 — Character Frequency Signature (Optimal & Implemented):**
   - For each string, count frequencies of `'a'` through `'z'` using a fixed `array<int, 26>`.
   - Build a delimiter-separated signature string (e.g. `"#1#0#0#0#1..."`).
   - Group the original strings in `unordered_map<string, vector<string>>`.
   - **Time:** $O(N \cdot K)$ — Linear with respect to total input characters.
   - **Space:** $O(N \cdot K)$ to store the hash map and results.
   - *Verdict:* Optimal asymptotic complexity; avoids sorting entirely.

---

## 3. Complexity Analysis
- **Time Complexity:** $O(N \cdot K)$
  - Counting characters in string of length $K$ takes $O(K)$.
  - Constructing the 26-element signature string takes $O(26) = O(1)$ constant time.
  - Hash map lookup/insertion takes average $O(K)$ time for string hashing.
  - Repeating for $N$ strings results in $O(N \cdot K)$ overall time.
- **Space Complexity:** $O(N \cdot K)$
  - The hash map stores all $N$ strings of length up to $K$.
  - Returning the final 2D vector requires $O(N \cdot K)$ auxiliary space.

---

## 4. Edge Cases & Gotchas
- [x] Empty string (`strs = [""]`): Produces a signature of 26 zeros (`#0#0...#0`), correctly grouping all empty strings together.
- [x] Single-character strings (`strs = ["a"]`): Correctly maps to its respective bucket.
- [x] **Key Ambiguity Pitfall:** Do not serialize counts without delimiters (e.g., `to_string(count[i])` without separator). Counts `[1, 23]` and `[12, 3]` would both produce `"123"`. Using a delimiter like `'#'` (`"#1#23"` vs `"#12#3"`) guarantees distinct signatures.

---

## 5. Clean Code (Frequency Signature — Optimal)

```cpp
class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        unordered_map<string, vector<string>> groups;

        for (const string& str : strs) {
            array<int, 26> count{};

            for (char c : str) {
                ++count[c - 'a'];
            }

            // Build an unambiguous signature: e.g. "#1#0#0#0#1..."
            string key;
            for (int i = 0; i < 26; ++i) {
                key += '#';
                key += to_string(count[i]);
            }

            groups[key].push_back(str);
        }

        vector<vector<string>> result;
        result.reserve(groups.size());

        for (auto& [key, group] : groups) {
            result.push_back(move(group)); // Move instead of copy for performance
        }

        return result;
    }
};
```

---

## 6. Review & Takeaways

### Alternative Implementation: Sorted String Key

When interviewing, if string lengths $K$ are small or time is tight, sorting each string is a valid and clean alternative:

```cpp
class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        unordered_map<string, vector<string>> groups;

        for (string str : strs) {
            string key = str;
            sort(key.begin(), key.end());
            groups[key].push_back(move(str));
        }

        vector<vector<string>> result;
        result.reserve(groups.size());

        for (auto& [key, group] : groups) {
            result.push_back(move(group));
        }

        return result;
    }
};
```

---

### 💡 C++ Interview Deep Dive

#### 1. Why use `string` as map key instead of `array<int, 26>`?
In C++, `std::unordered_map` provides built-in hash specialization for `std::string`, but **not** for `std::array<int, 26>`.
If you want to use `unordered_map<array<int, 26>, vector<string>>`, you must provide a custom hash functor. Converting the 26-count array into a delimiter-separated `string` is the standard, clean idiom in C++.

#### 2. Interview Pitch: *"Why this solution?"*
> *"I group strings based on their character frequency counts. Since the problem is constrained to lowercase English letters, every string can be canonically represented by a 26-element frequency signature. Anagrams generate identical signatures, allowing them to hash to the same bucket in an `unordered_map`. This achieves $O(N \cdot K)$ time complexity, which avoids the $O(N \cdot K \log K)$ cost of sorting each string."*

#### 3. Core Pattern Takeaway
* **Problem 1 (Two Sum):** Target Complement Lookup.
* **Problem 49 (Group Anagrams):** **Canonical Representation + Hashing**. Whenever you need to cluster items by equivalence, construct an invariant canonical key (sorted form or frequency signature) and group them with a hash map.

* **Next Review Date:** Medium priority (foundational string hashing pattern).
* **Key Takeaway:** Hash table grouping requires a canonical key. A delimited frequency signature provides optimal $O(N \cdot K)$ grouping for anagrams.
