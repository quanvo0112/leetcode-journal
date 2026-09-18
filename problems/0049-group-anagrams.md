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
  - Counting characters in a string of length $K$ takes $O(K)$.
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

## 5. Clean Code (Frequency Signature — Primary Solution)

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

### 🚀 Advanced Optimization: Direct 26-Byte Array Key with Custom Hash

In the primary solution, constructing `string key` requires:
1. Creating heap-allocated `string`.
2. Calling `to_string()` 26 times per word.
3. String concatenation.
4. Hashing the generated string in `unordered_map`.

We can eliminate all serialization overhead by using a compact **26-byte array** (`array<unsigned char, 26>`) directly as the map key with a custom polynomial rolling hash:

```cpp
class Solution {
    using Key = array<unsigned char, 26>;

    struct KeyHash {
        size_t operator()(const Key& key) const {
            size_t hash = 0;
            for (unsigned char c : key) {
                hash = hash * 31 + c; // Polynomial rolling hash
            }
            return hash;
        }
    };

public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        unordered_map<Key, vector<string>, KeyHash> groups;
        groups.reserve(strs.size());

        for (const string& str : strs) {
            Key count{};
            for (char c : str) {
                ++count[c - 'a'];
            }
            groups[count].push_back(str); // Zero string serialization
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

#### Why is `unsigned char` valid?
The problem constraint states `strs[i].length <= 100`. An `unsigned char` covers range $[0, 255]$, so each letter's count (at most 100) fits comfortably in **1 byte**. This keeps the entire key at just **26 bytes** on the stack with **zero heap allocations**.

---

### Alternative Implementation: Sorted String Key

When interviewing, if string lengths $K$ are small or time is constrained, sorting each string is concise and interview-friendly:

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

### 📊 Comparison of Approaches

| Approach | Time Complexity | Space Complexity | Pros & Cons |
| :--- | :---: | :---: | :--- |
| **1. Sort String Key** | $O(N \cdot K \log K)$ | $O(N \cdot K)$ | Shortest code, easiest to write in interviews. |
| **2. Frequency $\rightarrow$ String Key** | $O(N \cdot K)$ | $O(N \cdot K)$ | Linear asymptotic complexity, no custom hash required. |
| **3. Frequency $\rightarrow$ Array Key (Optimized)** | **$O(N \cdot K)$** | **$O(N \cdot K)$** | **Fastest in practice, zero string allocation/serialization overhead.** |

---

### 💡 C++ Interview & Engineering Mindset

1. **Don't Obsess Over Raw Milliseconds (e.g. 50ms vs 20ms):**
   LeetCode runtime fluctuations are heavily influenced by judge server load and test harness variations. What interviewers care about is **asymptotic scaling** ($O(N \cdot K)$ vs $O(N \cdot K \log K)$) and avoiding unnecessary allocations.

2. **The Core Pattern:**
   $$\text{Group Anagrams} \longrightarrow \text{Order doesn't matter} \longrightarrow \text{Canonical Representation} \longrightarrow \text{Frequency Table [26]} \longrightarrow \text{Hash Map}$$

3. **Interview Rule of Thumb:**
   - **Problem 1 (Two Sum):** Target Complement Lookup.
   - **Problem 49 (Group Anagrams):** **Canonical Representation + Hashing**. Whenever you need to cluster items by equivalence, construct an invariant canonical key and group them using a hash map.

* **Next Review Date:** Medium priority (foundational string hashing pattern).
* **Key Takeaway:** Hash table grouping requires a canonical key. Using `array<unsigned char, 26>` with a custom hash eliminates serialization overhead while keeping memory footprint to just 26 bytes.
