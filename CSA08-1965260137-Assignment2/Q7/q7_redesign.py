"""Q7 - Diagnose, redesign, validate. Chosen program: Q6 plain recursion ways_naive.
Author: M Ayaan (1965260137) | CSA0809"""
import time, statistics, csv, sys
sys.set_int_max_str_digits(0)
from collections import Counter

# ---------------- ORIGINAL ----------------
calls = 0; additions = 0
def ways_naive(n):
    global calls, additions
    calls += 1
    if n <= 1:
        return 1
    additions += 1
    return ways_naive(n - 1) + ways_naive(n - 2)

# ---------------- REDESIGN: bottom-up, keep only the last two values ----------------
def ways_fast(n):
    """Exploits: ways(n) depends only on ways(n-1) and ways(n-2)."""
    adds = 0
    prev, cur = 1, 1
    for _ in range(n - 1):
        prev, cur = cur, prev + cur
        adds += 1
    return (cur if n >= 1 else 1), adds

# ---------------- Multi-query redesign: one pass gives every n up to N ----------------
def ways_table(N):
    t = [1, 1]
    for i in range(2, N + 1):
        t.append(t[-1] + t[-2])
    return t

# ---------------- Diagnosis helpers ----------------
repeat_counter = Counter()
def ways_traced(n):
    repeat_counter[n] += 1
    if n <= 1:
        return 1
    return ways_traced(n - 1) + ways_traced(n - 2)

def best_time(fn, *a, repeat=3):
    ts = []
    for _ in range(repeat):
        t = time.perf_counter(); fn(*a); ts.append(time.perf_counter() - t)
    return statistics.mean(ts)

if __name__ == "__main__":
    print("A. DIAGNOSIS (n = 30)")
    ways_traced(30)
    print("  distinct sub-problems:", len(repeat_counter), "| total calls:", sum(repeat_counter.values()))
    for k in (30, 25, 20, 15, 10, 5, 2, 1, 0):
        print(f"  w({k}) evaluated {repeat_counter[k]} times")
    print("  share of calls that are w(1) or w(0):",
          f"{(repeat_counter[1]+repeat_counter[0])/sum(repeat_counter.values())*100:.1f}%")

    print("\nE. ORIGINAL vs REDESIGN (same inputs)")
    rows = []
    header = ["n", "naive_calls", "naive_adds", "fast_adds", "naive_time_s", "fast_time_s", "same_answer"]
    print(" | ".join(f"{h:>13}" for h in header))
    for n in (10, 20, 25, 30, 32, 35):
        calls = 0; additions = 0
        ans_n = ways_naive(n); c, a = calls, additions
        ans_f, fa = ways_fast(n)
        tn = best_time(ways_naive, n, repeat=3 if n <= 30 else 1)
        tf = best_time(ways_fast, n, repeat=50)
        row = [n, c, a, fa, round(tn, 5), round(tf, 8), ans_n == ans_f]
        rows.append(row)
        print(" | ".join(f"{x!s:>13}" for x in row))
    with open("q7_results.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)

    print("\nRedesign alone at large n (naive impossible):")
    for n in (1000, 10_000, 50_000):
        t = best_time(ways_fast, n, repeat=3)
        ans, adds = ways_fast(n)
        print(f"  n={n:<6} additions={adds:<6} time={t:.6f} s digits={len(str(ans))}")

    print("\nTrust print ways for EVERY n = 1..1000 (multi-query use case):")
    t = time.perf_counter()
    for n in range(1, 1001):
        ways_fast(n)
    t_each = time.perf_counter() - t
    t = time.perf_counter(); table = ways_table(1000); t_table = time.perf_counter() - t
    adds_each = sum(range(0, 1000))
    print(f"  fast per-n : additions={adds_each} time={t_each:.4f} s")
    print(f"  one table  : additions=999 time={t_table:.4f} s")
    print("  table matches fast:", all(table[n] == ways_fast(n)[0] for n in range(1, 1001)))
    print("  table memory cells =", len(table), "(O(n) trade-off vs O(1))")

    print("\nObjective check: calls/additions <= n and time < 1 ms at n=1000:",
          ways_fast(1000)[1] <= 1000 and best_time(ways_fast, 1000) < 0.001)
