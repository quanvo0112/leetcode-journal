# 0981. Time Based Key-Value Store

- **Problem Link:** https://leetcode.com/problems/time-based-key-value-store/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Binary Search`
- **LeetCode Topics:** `Hash Table` / `String` / `Binary Search` / `Design`
- **Core Pattern:** `Hash Map of Chronological Vectors + Rightmost Binary Search (Largest Timestamp <= Query)`
- **Last Practiced:** 2026-09-27
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - Design a time-based key-value data structure that stores multiple values for the same key at different timestamps.
  - `void set(String key, String value, int timestamp)` stores `key` with `value` at given `timestamp`.
  - `String get(String key, int timestamp)` returns a value such that `set` was called previously with `timestamp_prev <= timestamp`.
  - If multiple such values exist, return the value associated with the **largest `timestamp_prev`**. If no values exist, return `""`.
  - **Crucial Invariant in Constraints:** *"All the timestamps of `set` are strictly increasing."*
- **Core intuition:**
  - Because timestamps arrive in strictly ascending chronological order for each key, appending to a dynamic array (`vector<pair<int, string>>`) naturally preserves sorted order in amortized $O(1)$ time without requiring sort operations.
  - To answer `get(key, timestamp)`, we query the sorted vector for the **rightmost entry whose timestamp is $\le \text{query timestamp}$**.
  - This is the textbook **Rightmost Element Binary Search** pattern on a sorted collection.

---

## 2. Approach & Trade-offs

1. **Approach 1 — `unordered_map<string, map<int, string>>` ($O(\log M)$ `set`, $O(\log M)$ `get`):**
   - Store entries inside an ordered balanced binary search tree (`std::map`) per key.
   - Use `upper_bound(timestamp)` and take `std::prev`.
   - *Verdict:* Valid, but introduces unnecessary tree rebalancing overhead on every insertion when timestamps are already guaranteed to arrive monotonically sorted.

2. **Approach 2 — `unordered_map<string, vector<pair<int, string>>>` with `std::upper_bound` ($O(1)$ `set`, $O(\log M)$ `get`):**
   - Append to vector, use `std::upper_bound` with a custom comparator on pairs.
   - *Verdict:* Computationally efficient, but writing and remembering custom comparator lambdas for pairs is prone to syntax errors during technical interviews.

3. **Approach 3 — `unordered_map<string, vector<pair<int, string>>>` with Explicit Rightmost Binary Search (Chosen Optimal Solution):**
   - `set()` simply appends `{timestamp, value}` to `store[key]` in $O(1)$ amortized time.
   - `get()` performs explicit iterative binary search:
     - Search interval: `left = 0`, `right = values.size() - 1`.
     - Initialize `result = ""`.
     - While `left <= right`:
       - If `values[mid].first <= timestamp`:
         - `result = values[mid].second` (record viable candidate).
         - `left = mid + 1` (greedily search rightward for a larger valid timestamp).
       - Else:
         - `right = mid - 1` (timestamp too large, search left).
   - *Verdict:* Optimal $O(1)$ amortized `set` and $O(\log M)$ `get`. Zero tree overhead, clean and interview-friendly mental model.

---

## 3. Complexity Analysis

- **Time Complexity:**
  - **`set(key, value, timestamp)`:** $O(1)$ amortized. Appending to a `std::vector` takes amortized constant time; hash map lookup by string takes average $O(L)$ where $L$ is the key length ($L \le 10$).
  - **`get(key, timestamp)`:** $O(\log M)$ where $M$ is the number of historical timestamps recorded for the given `key`. Binary search halves the candidate space each iteration.
- **Space Complexity:** $O(N)$
  - Stores all $(key, value, timestamp)$ tuples across all invocations. Total space is proportional to the total number of `set` operations.

---

## 4. Edge Cases & Gotchas

- [x] **Key Does Not Exist:**
  - `if (!store.count(key)) return "";` guards against creating empty vector entries on non-existent keys.
- [x] **Query Timestamp is Smaller Than Earliest Timestamp (`timestamp < values[0].first`):**
  - The condition `values[mid].first <= timestamp` is never satisfied.
  - `right` repeatedly contracts to `-1`, loop exits, and `result` remains initialized to `""`, returning the correct empty string.
- [x] **Query Timestamp Matches Exact Entry:**
  - `values[mid].first <= timestamp` triggers on exact match, saves `result`, and checks right to ensure no duplicate timestamps exist (guaranteed unique by problem constraints).
- [x] **Query Timestamp Larger Than Latest Timestamp:**
  - Binary search sweeps all the way to `right = values.size() - 1`, returning the latest recorded value.

---

## 5. Clean Code (Optimal Solution: Hash Map + Rightmost Binary Search)

```cpp
#include <string>
#include <vector>
#include <unordered_map>

using namespace std;

class TimeMap {
private:
    // Maps each key to a sorted list of (timestamp, value) pairs
    unordered_map<string, vector<pair<int, string>>> store;

public:
    TimeMap() {
    }

    void set(string key, string value, int timestamp) {
        // Timestamps arrive in strictly increasing order; appending preserves sorted invariant
        store[key].push_back({timestamp, value});
    }

    string get(string key, int timestamp) {
        if (!store.count(key)) {
            return "";
        }

        const auto& values = store[key];
        int left = 0;
        int right = static_cast<int>(values.size()) - 1;
        string result = "";

        // Find the rightmost entry where entry.timestamp <= query timestamp
        while (left <= right) {
            int mid = left + (right - left) / 2;

            if (values[mid].first <= timestamp) {
                result = values[mid].second; // Viable candidate recorded
                left = mid + 1;              // Continue searching right for a larger timestamp
            } else {
                right = mid - 1;             // Timestamp exceeds query, search left
            }
        }

        return result;
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given operations:
```text
set("foo", "bar1", 1)
set("foo", "bar2", 4)
set("foo", "bar3", 8)
get("foo", 3)
```

In memory:
```text
"foo" -> [(1, "bar1"), (4, "bar2"), (8, "bar3")]
```

Query: `get("foo", 3)`:
```text
Initial range: left = 0, right = 2, result = ""

Iteration 1:
  mid = 0 + (2 - 0) / 2 = 1
  values[1] = (4, "bar2")
  Comparison: 4 <= 3 (values[mid].first <= timestamp) -> FALSE (4 > 3)
  -> Timestamp 4 is too large; search left.
  -> right = mid - 1 = 0
  Active range: [0, 0]

Iteration 2:
  mid = 0 + (0 - 0) / 2 = 0
  values[0] = (1, "bar1")
  Comparison: 1 <= 3 (values[mid].first <= timestamp) -> TRUE
  -> Timestamp 1 is valid!
  -> Record candidate: result = "bar1"
  -> Try searching right for an even larger valid timestamp:
  -> left = mid + 1 = 1
  Active range: [1, 0]

Loop terminates (left > right).
Return result: "bar1".
```

---

### The Architectural Pattern

```text
                  Time Based Key-Value Store
                              ↓
              unordered_map<string, vector<pair<int, string>>>
                              ↓
           set(key, val, ts) ──> store[key].push_back({ts, val})  [O(1)]
                              ↓
           get(key, query_ts):
             left = 0, right = n - 1, result = ""
                              ↓
                     while left <= right:
                              ↓
                  mid.timestamp <= query_ts ?
                         /        \
                   YES  /          \  NO
                       ↓            ↓
               result = mid.val    right = mid - 1
               left = mid + 1      (Too large, go left)
             (Try finding larger
              timestamp on right)
```

* **Next Review Date:** Low priority (benchmark rightmost binary search on chronological streams mastered).
* **Key Takeaway:** When event logs or time series arrive in chronological order, use an `unordered_map` with dynamic vectors instead of balanced trees to achieve $O(1)$ appends and $O(\log M)$ queries via rightmost binary search (`left = mid + 1` upon match).
