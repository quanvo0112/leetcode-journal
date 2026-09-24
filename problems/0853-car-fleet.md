# 0853. Car Fleet

- **Problem Link:** https://leetcode.com/problems/car-fleet/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Stack`
- **LeetCode Topics:** `Array` / `Stack` / `Sorting` / `Monotonic Stack`
- **Core Pattern:** `Sort by Position Descending + Greedy Fleet Merging with Fractional Arrival Time`
- **Last Practiced:** 2026-09-24
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - $n$ cars are traveling to the same destination `target` along a one-lane road.
  - A car can never pass another car ahead of it. If a faster car catches up to a slower car, it slows down to match the speed of the car ahead, forming a single "car fleet".
  - A car that catches up to a fleet at the exact `target` is still considered part of that fleet.
  - Return the total number of car fleets that arrive at the destination.
- **Core intuition:**
  - Because cars cannot overtake each other, **position order dictates precedence**. The car closest to `target` faces zero obstacles ahead—it sets the maximum pace for everything behind it.
  - If we process cars from **closest to target to farthest from target** (descending position order), each car behind can be evaluated independently:
    $$\text{Arrival Time} = \frac{\text{target} - \text{position}}{\text{speed}}$$
  - If a trailing car arrives in **less than or equal to** the time of the fleet directly ahead ($\text{time} \le \text{fleetTime}$), it will catch up before or at `target`. It gets absorbed into that fleet and assumes that fleet's speed.
  - If a trailing car arrives strictly **later** ($\text{time} > \text{fleetTime}$), it can never catch up. It becomes the leader of a brand new fleet, setting a new arrival benchmark for subsequent cars further behind.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Time-Step Simulation ($O(N \cdot \text{Target})$ Time):**
   - Simulate cars moving forward frame by frame or collision by collision.
   - *Verdict:* Completely infeasible for constraints where $N \le 10^5$, $\text{target} \le 10^6$.

2. **Approach 2 — Sort + Monotonic Stack of `double` ($O(N \log N)$ Time, $O(N)$ Space):**
   - Sort cars descending by position.
   - Push arrival times `(double)(target - pos) / speed` onto a `std::stack<double>`.
   - If current time is $\le$ top of stack, pop it (absorbed into the lead fleet).
   - *Verdict:* Valid, but using floating-point `double` risks precision rounding errors, and allocating an explicit `stack` container is redundant because we only ever query the arrival time of the single fleet directly ahead.

3. **Approach 3 — Sort Descending + Fractional Arrival Time Greedy (Chosen Optimal Solution):**
   - Pair each car as `(position, speed)` and sort in descending order of position.
   - Maintain the arrival time of the fleet ahead as an exact fraction: $\frac{\text{fleetDistance}}{\text{fleetSpeed}}$.
   - For each trailing car with distance $d = \text{target} - \text{pos}$ and speed $\text{spd}$:
     $$\frac{d}{\text{spd}} > \frac{\text{fleetDistance}}{\text{fleetSpeed}} \iff d \times \text{fleetSpeed} > \text{fleetDistance} \times \text{spd}$$
   - If true: The car arrives later and cannot catch up $\implies$ increment `fleets`, update lead fleet fraction to $(\text{distance}, \text{speed})$.
   - Otherwise: The car catches up before or at `target` $\implies$ absorbed into current fleet with no change to the lead fleet arrival time.
   - *Verdict:* Optimal $O(N \log N)$ Time, $O(N)$ Space. Pure integer arithmetic eliminates floating-point bugs; variable tracking eliminates stack container overhead.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N \log N)$
  - Sorting $N$ pairs by position takes $O(N \log N)$ time.
  - The subsequent single pass through all cars takes $O(N)$ time with $O(1)$ operations per car.
  - Overall Time: $O(N \log N)$.
- **Space Complexity:** $O(N)$
  - Storing the paired `cars` vector requires $O(N)$ auxiliary memory.
  - Only $O(1)$ additional scalar variables (`fleets`, `fleetDistance`, `fleetSpeed`) are used during the greedy pass.

---

## 4. Edge Cases & Gotchas

- [x] **Catching up at the exact target:**
  - Cars arriving at the identical moment belong to the same fleet.
  - The condition to spawn a new fleet must be strictly greater than (`>`): `d * fleetSpeed > fleetDistance * spd`. Using `>=` would incorrectly split fleets that meet at the target line.
- [x] **64-bit Integer Overflow Protection:**
  - Constraints: $\text{target} \le 10^6$, $\text{speed} \le 10^6 \implies \text{distance} \times \text{fleetSpeed} \le 10^6 \times 10^6 = 10^{12}$.
  - $10^{12}$ exceeds standard 32-bit signed integer limits ($2 \times 10^9$). Using `long long` for distance, speed, and cross-multiplications is mandatory to prevent integer overflow.
- [x] **Single Car Input ($N = 1$):**
  - Instantly forms a single fleet and returns 1 correctly.
- [x] **Cars Starting in Arbitrary Order:**
  - Problem input does not guarantee sorted order of `position`. Sorting descending is a mandatory prerequisite.

---

## 5. Clean Code (Optimal Solution: Sort Descending + Fractional Greedy)

```cpp
#include <vector>
#include <algorithm>

using namespace std;

class Solution {
public:
    int carFleet(int target, vector<int>& position, vector<int>& speed) {
        int n = position.size();
        vector<pair<int, int>> cars;
        cars.reserve(n);

        for (int i = 0; i < n; ++i) {
            cars.push_back({position[i], speed[i]});
        }

        // Process cars from closest to target to farthest from target
        sort(cars.begin(), cars.end(), [](const auto& a, const auto& b) {
            return a.first > b.first;
        });

        int fleets = 0;
        // Arrival time of the fleet directly ahead represented as fraction: fleetDistance / fleetSpeed
        long long fleetDistance = 0;
        long long fleetSpeed = 1;
        bool hasFleet = false;

        for (const auto& [pos, spd] : cars) {
            long long distance = target - pos;

            if (!hasFleet) {
                ++fleets;
                fleetDistance = distance;
                fleetSpeed = spd;
                hasFleet = true;
                continue;
            }

            // distance / spd > fleetDistance / fleetSpeed
            // <=> distance * fleetSpeed > fleetDistance * spd
            // This car arrives later than the fleet ahead -> cannot catch up -> forms a new fleet
            if (distance * fleetSpeed > fleetDistance * spd) {
                ++fleets;
                fleetDistance = distance;
                fleetSpeed = spd;
            }
            // Otherwise, this car catches up before or at target and joins the fleet ahead
        }

        return fleets;
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given `target = 12`, `position = [10, 8, 5, 3, 0]`, `speed = [2, 4, 1, 3, 1]`:

```text
After sorting descending by position:
Cars: (pos=10, spd=2), (pos=8, spd=4), (pos=5, spd=1), (pos=3, spd=3), (pos=0, spd=1)

Car 1: pos=10, spd=2, distance = 12 - 10 = 2
  - No fleet ahead yet -> Spawns Fleet #1.
  - fleetDistance = 2, fleetSpeed = 2 (Arrival Time = 2 / 2 = 1.0)
  - fleets = 1

Car 2: pos=8, spd=4, distance = 12 - 8 = 4
  - Compare arrival: (4 * 2) > (2 * 4) <=> 8 > 8 (FALSE)
  - Time is <= fleetTime (1.0 <= 1.0) -> Catches up at target!
  - Joins Fleet #1.

Car 3: pos=5, spd=1, distance = 12 - 5 = 7
  - Compare arrival: (7 * 2) > (2 * 1) <=> 14 > 2 (TRUE)
  - Time is > fleetTime (7.0 > 1.0) -> Cannot catch up!
  - Spawns Fleet #2.
  - fleetDistance = 7, fleetSpeed = 1 (Arrival Time = 7 / 1 = 7.0)
  - fleets = 2

Car 4: pos=3, spd=3, distance = 12 - 3 = 9
  - Compare arrival: (9 * 1) > (7 * 3) <=> 9 > 21 (FALSE)
  - Time is <= fleetTime (3.0 <= 7.0) -> Catches up before target!
  - Joins Fleet #2.

Car 5: pos=0, spd=1, distance = 12 - 0 = 12
  - Compare arrival: (12 * 1) > (7 * 1) <=> 12 > 7 (TRUE)
  - Time is > fleetTime (12.0 > 7.0) -> Cannot catch up!
  - Spawns Fleet #3.
  - fleetDistance = 12, fleetSpeed = 1 (Arrival Time = 12.0)
  - fleets = 3

Final Result: 3 car fleets.
```

---

### The Architectural Pattern

```text
                         Car Fleet
                            ↓
                Sort by Position Descending
              (Closest to Target -> Farthest)
                            ↓
                Calculate Arrival Time Ratio:
                   time = distance / speed
                            ↓
         Compare with Fleet Ahead (via cross-multiplication):
           distance * fleetSpeed > fleetDistance * speed ?
                  /                                \
             YES /                                  \ NO
                ↓                                    ↓
       Cannot Catch Up                         Catches Up
  (Spawns new fleet; becomes              (Absorbed into current
   new lead fleet reference)               fleet; no time update)
```

* **Next Review Date:** Low priority (benchmark physical sorting + greedy barrier absorption pattern mastered).
* **Key Takeaway:** When faster elements behind are physically bottlenecked by slower elements ahead, sort from the destination backward so that lead blockers are resolved first. Use cross-multiplied fractions to prevent precision degradation.
