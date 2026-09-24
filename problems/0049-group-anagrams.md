# 0049. Group Anagrams

- **Problem Link:** https://leetcode.com/problems/group-anagrams/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Arrays & Hashing`
- **LeetCode Topics:** `Array` / `Hash Table` / `String` / `Sorting`
- **Core Pattern:** `Categorize by Sorted String / Frequency Array Hash Key`
- **Last Practiced:** 2026-09-18
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers
- Clues in prompt: *"group the anagrams together"*, *"lowercase English letters"*, *"strs.length <= 10^4"*, *"strs[i].length <= 100"*.
- Core intuition: Two strings are anagrams if and only if they possess identical character frequencies. Since character ordering does not matter, we map each string to a **canonical representation** (a 26-element frequency signature). By using this 26-byte signature directly as a hash key, all anagrams naturally land in the same hash-map bucket without any sorting or string serialization overhead.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Sort Each String ($O(N \cdot K \log K)$):**
   - Sort each word alphabetically (`"eat"` $\rightarrow$ `"aet"`) and use the sorted string as the hash map key.
   - *Verdict:* Easiest to write and shortest code, but asymptotically slower due to the $O(K \log K)$ sorting step per string.

2. **Approach 2 — Frequency $\rightarrow$ Serialized String Key ($O(N \cdot K)$):**
   - Count frequencies into an array, then serialize to a delimiter-separated string (e.g., `"#1#0#0...#1"`).
   - *Verdict:* Linear time complexity, but incurs overhead from multiple `to_string()` calls, string allocations, concatenations, and hashing a dynamic string.

3. **Approach 3 — 26-Byte Frequency Array Directly as Map Key (Optimal & Implemented):**
   - Use `array<unsigned char, 26>` directly as the hash key in `unordered_map` with a custom polynomial rolling hash.
   - *Verdict:* Pure $O(N \cdot K)$ time complexity. Zero heap allocation for keys, zero string serialization, cache-friendly, and optimal memory footprint.

---

## 3. Complexity Analysis
Let $N$ be the number of strings (`strs.size()`) and $K$ be the maximum string length (`strs[i].size() \le 100`).

- **Time Complexity:** $O(N \cdot K)$
  - Character counting per string: $O(K)$.
  - Hashing the 26-byte key: $O(26) = O(1)$ constant time.
  - Total for $N$ strings: $O(N \cdot K)$.
- **Space Complexity:** $O(N \cdot K)$
  - Hash map storage: $N$ keys of fixed size 26 bytes on the stack ($O(26N) = O(N)$), plus the grouped strings ($O(N \cdot K)$).
  - Total auxiliary space: $O(N \cdot K)$ for output and groups.

---

## 4. Edge Cases & Gotchas
- [x] **Empty string (`strs = [""]`):** Produces an array of 26 zeros (`count = {0}`), correctly grouping all empty strings together.
- [x] **Single-character strings (`strs = ["a"]`):** Correctly increments `count[0]` and buckets properly.
- [x] **Is `unsigned char` safe from overflow?** Yes. The constraint states `strs[i].length <= 100`. An `unsigned char` spans $[0, 255]$, so even if a string consists entirely of 100 identical characters (e.g. `"aaaa..."`), the maximum frequency is 100, fitting comfortably within 1 byte.

---

## 5. Clean Code (Optimal Solution: 26-Byte Array Key + Custom Hash)

```cpp
class Solution {
    using Key = array<unsigned char, 26>;

    struct KeyHash {
        size_t operator()(const Key& key) const {
            size_t hash = 0;

            for (unsigned char c : key) {
                hash = hash * 31 + c;
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

            groups[count].push_back(str);
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

## 6. Review & Takeaways

### Why This Solution Outperforms Other Approaches

In common solutions, people often serialize counts into a `string`:
```cpp
string key;
for (int i = 0; i < 26; ++i) {
    key += '#';
    key += to_string(count[i]);
}
```
This forces:
1. Creating heap-allocated `string` objects.
2. 26 calls to `to_string()`.
3. Multiple string reallocations/concatenations.
4. `unordered_map` having to hash the resulting dynamic string.

By switching to `using Key = array<unsigned char, 26>`, we eliminate all of this:
- **Zero dynamic memory allocation** for keys (26 bytes directly on the stack).
- **Zero serialization overhead** (no `to_string`, no `+` operators).
- A fast, predictable polynomial rolling hash (`hash * 31 + c`).

---

### Alternative Implementations for Reference

#### 1. Sort Each String (Easiest in Interviews)
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

#### 2. Frequency Count $\rightarrow$ String Key (Standard Non-Custom Hash)
```cpp
class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        unordered_map<string, vector<string>> groups;

        for (const string& str : strs) {
            array<int, 26> count{};
            for (char c : str) ++count[c - 'a'];

            string key;
            for (int i = 0; i < 26; ++i) {
                key += '#';
                key += to_string(count[i]);
            }
            groups[key].push_back(str);
        }

        vector<vector<string>> result;
        result.reserve(groups.size());
        for (auto& [key, group] : groups) result.push_back(move(group));
        return result;
    }
};
```

---

### Summary of Approaches

| Approach | Time Complexity | Space Complexity | Description |
| :--- | :---: | :---: | :--- |
| **1. Sort String Key** | $O(N \cdot K \log K)$ | $O(N \cdot K)$ | Easiest to write, shortest code. |
| **2. Frequency $\rightarrow$ String Key** | $O(N \cdot K)$ | $O(N \cdot K)$ | Linear asymptotic complexity, standard interview-friendly. |
| **3. Frequency $\rightarrow$ Array Key (Optimal Choice)** | **$O(N \cdot K)$** | **$O(N \cdot K)$** | **Optimal in practice: Zero heap allocations for keys, zero string serialization.** |

---

### Engineering Mindset & Interview Takeaways

1. **Don't Obsess Over Raw Milliseconds (e.g. 50ms vs 20ms):**
   LeetCode runtime measurements exhibit substantial variance based on judge server load and harness execution. 50ms does not mean an algorithm is bad. What matters in interviews and production is:
   - Asymptotic scaling: $O(N \cdot K)$ vs $O(N \cdot K \log K)$.
   - Eliminating unnecessary heap allocations and redundant serialization.

2. **The Core Architectural Pattern:**
   ```text
   Group Anagrams
        ↓
   Recognize: Order doesn't matter
        ↓
   Create canonical representation
        ↓
   Character frequency signature [26]
        ↓
   Hash Map
   ```

3. **Rule of Thumb:**
   - **Two Sum:** `unordered_map` (Target Complement Lookup).
   - **Group Anagrams:** Frequency Signature + `unordered_map` (**Canonical Representation + Hashing**).

* **Next Review Date:** Medium priority (foundational canonical hashing pattern).
* **Key Takeaway:** When grouping by equivalence, design an invariant canonical key. Using a compact fixed-size array (`array<unsigned char, 26>`) with a custom hash eliminates string serialization entirely.
