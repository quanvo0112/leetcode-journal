# 0271. Encode and Decode Strings

- **Problem Link:** [NeetCode](https://neetcode.io/problems/string-encode-and-decode) / [LeetCode](https://leetcode.com/problems/encode-and-decode-strings/)
- **Difficulty:** `Medium`
- **Topic / Pattern:** `Array` / `String` / `Design` / `Serialization`
- **Last Practiced:** 2026-09-18
- **Proficiency Level:** 
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers
- Clues in prompt: *"design an algorithm to encode a list of strings to a single string"*, *"strings can contain any of the 256 possible ASCII characters"*, *"stateless design"*.
- Core intuition: Because strings may contain any character (including delimiters like `,`, `#`, spaces, or newlines), no single character can be assumed absent from input. Therefore, delimiter-based separation alone is ambiguous. We must use **Length-Prefix Framing** (`[length]#[payload]`). The delimiter `#` acts solely as a separator between the *length metadata* and the *raw string payload*, allowing the decoder to jump forward by exactly `length` bytes regardless of payload contents.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Static Delimiter (Naive & Broken):**
   - Append a special character between strings (e.g., `"hello#world#"`).
   - *Failure:* If any input string contains `#` (e.g., `["a#b", "hello"]` $\rightarrow$ `"a#b#hello#"`), the decoder cannot distinguish between a delimiter and part of the string.

2. **Approach 2 — Escaping Delimiters (Complex):**
   - Escape every delimiter occurrence (e.g. replace `#` with `\#`, and `\` with `\\`).
   - *Trade-off:* Requires multiple scan passes, increases string size, and is prone to edge-case parsing bugs.

3. **Approach 3 — Length-Prefix Encoding (Optimal & Implemented):**
   - **Encode:** Format each string as `[length]#[string]` (e.g. `"5#Hello5#World"`).
   - **Decode:** Read the numeric characters up to `#` to obtain `length`, skip the `#`, extract exactly `length` characters as the string, and advance the index.
   - *Verdict:* Completely unambiguous, handles all 256 ASCII characters, single pass, optimal $O(M)$ runtime.

---

## 3. Complexity Analysis
Let $M$ be the total number of characters across all strings, and $N$ be the number of strings (`strs.size()`).

- **Time Complexity:**
  - `encode`: $O(M)$ — Single pass over each string to concatenate its length digits, delimiter, and payload characters.
  - `decode`: $O(M)$ — Single traversal through the serialized string; each character is processed in constant time.
  - Total Time: **$O(M)$** linear time.
- **Space Complexity:** $O(M + N)$
  - The encoded string requires $M + \sum \text{digits}(\text{length}_i) + N \approx O(M + N)$ space.
  - The decoded vector holds the reconstructed strings ($O(M)$ space).

---

## 4. Edge Cases & Gotchas
- [x] **Empty collection (`strs = []`):** Encodes to `""`, loop does not run, returns empty vector `[]`.
- [x] **Empty string in array (`strs = [""]`):** Encodes to `"0#"`. Decoder parses `length = 0`, skips `#`, extracts `s.substr(i, 0)` which is `""`, advancing correctly.
- [x] **Strings containing `#`:** e.g., `["#abc", "a#b"]` $\rightarrow$ Encodes to `"4##abc3#a#b"`. The decoder reads `4`, skips the first `#`, and grabs `"#abc"` verbatim without being confused by the `#` inside the payload.
- [x] **Strings of purely numeric characters:** e.g., `["123", "45"]` $\rightarrow$ Encodes to `"3#1232#45"`. The `#` clearly demarcates metadata from payload.

---

## 5. Clean Code (Length-Prefix Framing — Optimal)

```cpp
class Solution {
public:
    string encode(vector<string>& strs) {
        string encoded;

        for (const string& str : strs) {
            encoded += to_string(str.size());
            encoded += '#';
            encoded += str;
        }

        return encoded;
    }

    vector<string> decode(string s) {
        vector<string> result;
        int i = 0;

        while (i < s.size()) {
            int length = 0;

            // Parse length on-the-fly to avoid substr() and stoi() allocations
            while (s[i] != '#') {
                length = length * 10 + (s[i] - '0');
                ++i;
            }
            ++i; // Skip the delimiter '#'

            result.push_back(s.substr(i, length));
            i += length; // Jump forward by exactly 'length' characters
        }

        return result;
    }
};
```

---

## 6. Review & Takeaways

### Dry Run Walkthrough

```text
Input: strs = {"neet", "code", "#abc", ""}

1. Encoding:
   "neet" -> "4#neet"
   "code" -> "4#code"
   "#abc" -> "4##abc"
   ""     -> "0#"
   Encoded Output: "4#neet4#code4##abc0#"

2. Decoding:
   i = 0: reads '4', hits '#', extracts next 4 chars -> "neet"  (i advances to 6)
   i = 6: reads '4', hits '#', extracts next 4 chars -> "code"  (i advances to 12)
   i = 12: reads '4', hits '#', extracts next 4 chars -> "#abc" (i advances to 18)
   i = 18: reads '0', hits '#', extracts next 0 chars -> ""     (i advances to 20)
   Terminates: result = ["neet", "code", "#abc", ""]
```

---

### Alternative Implementation: Using `stoi` & `substr`

While functionally identical, parsing the integer manually in the primary solution is cleaner in C++ as it avoids creating temporary substring objects:

```cpp
class Solution {
public:
    string encode(vector<string>& strs) {
        string encoded;
        for (const string& str : strs) {
            encoded += to_string(str.size()) + '#' + str;
        }
        return encoded;
    }

    vector<string> decode(string s) {
        vector<string> result;
        int i = 0;

        while (i < s.size()) {
            int j = i;
            while (s[j] != '#') ++j;

            int length = stoi(s.substr(i, j - i));
            result.push_back(s.substr(j + 1, length));
            i = j + 1 + length;
        }

        return result;
    }
};
```

---

### C++ Backend & Systems Architecture Takeaway

1. **Protocol Framing & Serialization:**
   This problem is an abstraction of real-world communication protocols:
   - **TCP Stream Framing:** Raw byte streams have no intrinsic message boundaries. Protocols prepend message length headers (or use Type-Length-Value / TLV in Protocol Buffers) so the receiver knows when a frame ends.
   - **HTTP/1.1 Chunked Transfer:** Uses `[chunk size in hex]\r\n[data]\r\n` to stream data of variable lengths.

2. **The Golden Engineering Principle:**
   > *"When a delimiter can legitimately appear in raw payload data, never use delimiter-based framing alone. Prepend payload length metadata."*

* **Next Review Date:** Low priority (standard serialization protocol).
* **Key Takeaway:** Length-prefix encoding (`[length]#[data]`) is the de-facto solution for serializing arbitrarily formatted byte streams without escaping or collision.

