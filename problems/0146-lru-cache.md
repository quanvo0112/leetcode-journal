# 0146. LRU Cache

- **Problem Link:** https://leetcode.com/problems/lru-cache/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Linked List`
- **LeetCode Topics:** `Hash Table` / `Linked List` / `Design` / `Doubly-Linked List`
- **Core Pattern:** `Hash Map + Doubly Linked List with Sentinel Nodes`
- **Last Practiced:** 2026-10-01
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - Design a data structure that follows the constraints of a **Least Recently Used (LRU)** cache.
  - Implement `get(key)` and `put(key, value)`.
  - Both operations must run in strict **$O(1)$ average time complexity**.
- **Core intuition — Combining Complementary Data Structures:**
  - **Fast Lookup ($O(1)$):** A hash table (`std::unordered_map<int, Node*>`) provides $O(1)$ average time key-to-node address resolution. However, hash tables do not maintain access order or relative recency.
  - **Fast Reordering & Splicing ($O(1)$):** A doubly linked list maintains chronological access order. Any node can be disconnected and repositioned in $O(1)$ time without shifting elements, provided we hold a direct pointer to that node.
  - **Why Doubly Linked (not Singly Linked)?**
    - Splicing out a node requires access to its predecessor: `node->prev->next = node->next`.
    - In a singly linked list, locating `node->prev` takes $O(N)$ linear traversal, failing the $O(1)$ requirement.
  - **The Recency Invariant:**
    - `head->next` points to the **Most Recently Used (MRU)** item.
    - `tail->prev` points to the **Least Recently Used (LRU)** item.
    - Accessing an existing item via either `get()` or `put()` immediately moves it to `head->next` (MRU).
    - Exceeding `capacity` triggers immediate eviction of `tail->prev` (LRU).
  - **Why Node Must Store `key`:**
    - When evicting `tail->prev`, we hold a pointer to the LRU node. To remove its corresponding entry from `cache`, we must know its key (`cache.erase(lru->key)`). Without storing `key` inside `Node`, reversing the lookup from `Node*` to key would require an $O(N)$ scan of the hash map.

---

## 2. Approaches & Trade-offs

1. **Approach 1 — Array / Vector + Timestamps ($O(1)$ get, $O(N)$ put/evict):**
   - Store entries with access timestamps in a flat vector.
   - *Drawback:* Finding the minimum timestamp during eviction requires scanning the entire cache ($O(N)$), violating $O(1)$.

2. **Approach 2 — Using `std::list` + `std::unordered_map` ($O(1)$ average, Idiomatic C++ STL):**
   - Store key-value pairs in `std::list<pair<int, int>>` and iterators in `std::unordered_map<int, list<pair<int,int>>::iterator>`.
   - Splice iterators to the front using `list::splice`.
   - *Drawback:* While clean and production-idiomatic, standard technical interviews specifically test whether you can design and implement node splicing and pointer manipulation manually.

3. **Approach 3 — Custom Doubly Linked List with Sentinel Head/Tail + `unordered_map` (Chosen Optimal Solution):**
   - Maintain explicit `head` and `tail` dummy sentinel nodes.
   - Encapsulate pointer mechanics in two atomic helpers:
     - `remove(Node* node)`: Unlinks `node` in $O(1)$.
     - `insertFront(Node* node)`: Inserts `node` immediately after `head` (MRU position) in $O(1)$.
   - Sentinel nodes eliminate all edge-case branching for empty lists, single-element lists, and head/tail boundary updates.
   - *Verdict:* Optimal $O(1)$ average time for both `get` and `put`, strict $O(\text{capacity})$ memory, and transparent, interview-grade pointer architecture.

---

## 3. Complexity Analysis

- **Time Complexity:**
  - `get(key)`: $O(1)$ average
    - Hash map lookup takes $O(1)$ average.
    - Pointer unlinking (`remove`) and insertion at head (`insertFront`) take $O(1)$ pointer assignments.
  - `put(key, value)`: $O(1)$ average
    - Hash map lookup takes $O(1)$ average.
    - If key exists: value update and relocation take $O(1)$.
    - If key is new: node allocation and insertion take $O(1)$. Evicting the LRU element (`tail->prev`) via `cache.erase()` and node deletion takes $O(1)$ average.
- **Space Complexity:** $O(\text{capacity})$
  - The cache stores at most `capacity` live nodes plus 2 sentinel nodes.
  - The hash map stores at most `capacity` key-to-pointer entries.

---

## 4. Edge Cases & Gotchas

- [x] **Capacity of 1 (`capacity = 1`):** Every insertion of a new key immediately evicts the previous single element. Sentinel nodes guarantee `tail->prev` correctly targets the single active element without null dereferences.
- [x] **Updating an existing key:** A `put()` with an existing key must update the value **and** promote the node to MRU (`head->next`). It must NOT increment size or trigger eviction.
- [x] **`get()` also updates recency:** Calling `get(key)` constitutes a cache access. The requested node must be moved to the MRU position.
- [x] **Memory Management:** Dynamically allocated nodes evicted during `put()` must be freed with `delete` to prevent memory leaks in production C++.
- [x] **Sentinel Invariant:** `head->prev` and `tail->next` remain `nullptr` at all times; client nodes are strictly situated between `head` and `tail`.

---

## 5. Clean Code

```cpp
#include <unordered_map>

using namespace std;

class LRUCache {
private:
    struct Node {
        int key;
        int value;
        Node* prev;
        Node* next;

        Node(int k, int v)
            : key(k), value(v), prev(nullptr), next(nullptr) {}
    };

    int capacity;
    unordered_map<int, Node*> cache;

    Node* head;
    Node* tail;

    void remove(Node* node) {
        node->prev->next = node->next;
        node->next->prev = node->prev;
    }

    void insertFront(Node* node) {
        node->next = head->next;
        node->prev = head;

        head->next->prev = node;
        head->next = node;
    }

public:
    LRUCache(int capacity) : capacity(capacity) {
        // Dummy head (MRU) / tail (LRU) sentinels
        head = new Node(0, 0);
        tail = new Node(0, 0);

        head->next = tail;
        tail->prev = head;
    }

    int get(int key) {
        if (cache.find(key) == cache.end()) {
            return -1;
        }

        Node* node = cache[key];

        // Recently accessed -> promote to MRU (front)
        remove(node);
        insertFront(node);

        return node->value;
    }

    void put(int key, int value) {
        // Case 1: Key already exists -> update value & promote to MRU
        if (cache.find(key) != cache.end()) {
            Node* node = cache[key];
            node->value = value;

            remove(node);
            insertFront(node);
            return;
        }

        // Case 2: New key -> create node, register in cache, insert at MRU
        Node* node = new Node(key, value);
        cache[key] = node;
        insertFront(node);

        // Case 3: Over capacity -> evict LRU (tail->prev)
        if (cache.size() > static_cast<size_t>(capacity)) {
            Node* lru = tail->prev;

            cache.erase(lru->key);
            remove(lru);
            delete lru;
        }
    }
};
```

---

## 6. Visual Walkthrough & Architectural Pattern

### Step-by-Step State Trace (`capacity = 2`)

```text
Initialize:
  head <---> tail
  cache: {}

1. put(1, 1):
  Create Node(1, 1). Insert front.
  head <---> [1:1] <---> tail
  cache: {1 -> Node(1)}

2. put(2, 2):
  Create Node(2, 2). Insert front.
  head <---> [2:2] <---> [1:1] <---> tail
             (MRU)       (LRU)
  cache: {1 -> Node(1), 2 -> Node(2)}

3. get(1):
  Found Node(1). Remove and insertFront(Node(1)).
  head <---> [1:1] <---> [2:2] <---> tail
             (MRU)       (LRU)
  Returns 1.

4. put(3, 3):
  Key 3 is new. Create Node(3, 3). Insert front.
  head <---> [3:3] <---> [1:1] <---> [2:2] <---> tail
  Size (3) > capacity (2) -> Evict LRU (tail->prev = Node(2)):
    - cache.erase(2)
    - remove(Node(2))
    - delete Node(2)
  head <---> [3:3] <---> [1:1] <---> tail
             (MRU)       (LRU)
  cache: {1 -> Node(1), 3 -> Node(3)}

5. get(2):
  Key 2 not in cache -> Returns -1.
```

---

### The Splicing Mechanics

```text
Removing a node B:
  A <=========> B <=========> C
  A <-----------------------> C
  node->prev->next = node->next;
  node->next->prev = node->prev;

Inserting node N at front (after head):
  head <====================> A
  head <---> [ N ] <--------> A
  node->next = head->next;
  node->prev = head;
  head->next->prev = node;
  head->next = node;
```

---

### The Architectural Pattern

```text
                           LRU Cache Architecture
                                     ↓
               ┌─────────────────────┴─────────────────────┐
               ↓                                           ↓
     std::unordered_map                           Doubly Linked List
  { key -> Node* pointer }                    head (MRU) <---> tail (LRU)
               ↓                                           ↓
         O(1) key lookup                              O(1) splice
               └─────────────────────┬─────────────────────┘
                                     ↓
                 get(key): lookup -> promote to head
                 put(key, val):
                   - if exists -> update val -> promote to head
                   - if new -> insert at head
                   - if size > cap -> evict tail->prev (LRU)
                                     ↓
                     O(1) Average Time per Operation
```

* **Next Review Date:** Low priority (standard canonical design pattern mastered).
* **Key Takeaway:** Pair a hash map for $O(1)$ random lookups with a doubly linked list equipped with dummy sentinels (`head` for MRU, `tail` for LRU) for $O(1)$ unlinking and re-insertion. Always store `key` inside the node to enable $O(1)$ hash map erasure during eviction.
