"""Q6 - Climbing temple steps. Author: M Ayaan (1965260137) | CSA0809"""
import sys, time
from functools import lru_cache

calls = 0

def ways_naive(n):
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)

@lru_cache(maxsize=None)
def ways_memo(n):
    global calls
    calls += 1
    if n <= 1:                      # TODO 1
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)

def ways_loop(n):
    prev, cur = 1, 1                # ways(0), ways(1)
    for _ in range(n - 1):
        prev, cur = cur, prev + cur
    return cur if n >= 1 else 1

def call_tree(n, depth=0):
    print("  " * depth + f"w({n})")
    if n > 1:
        call_tree(n - 1, depth + 1); call_tree(n - 2, depth + 1)

if __name__ == "__main__":
    calls = 0; print("naive:", ways_naive(25), "calls =", calls)
    ways_memo.cache_clear()
    calls = 0; print("memo :", ways_memo(25), "calls =", calls)

    print("\nHand-check n=1..6 (hand answers 1,2,3,5,8,13):")
    hand = [1, 2, 3, 5, 8, 13]
    for n, h in zip(range(1, 7), hand):
        print(f"  n={n}: hand={h} naive={ways_naive(n)} memo={ways_memo(n)} loop={ways_loop(n)}")

    print("\nCall tree for n=5:")
    call_tree(5)

    print("\nCall counts (prediction for naive: 2*ways(n)-1):")
    print(f"{'n':>3} {'naive calls':>12} {'predicted':>10} {'memo calls (fresh)':>20}")
    for n in (10, 20, 25, 30):
        calls = 0; ways_naive(n); c1 = calls
        ways_memo.cache_clear(); calls = 0; ways_memo(n); c2 = calls
        print(f"{n:>3} {c1:>12} {2*ways_loop(n)-1:>10} {c2:>20}")

    print("\nn=1000:")
    print("recursion limit:", sys.getrecursionlimit())
    ways_memo.cache_clear()
    try:
        ways_memo(1000)
        print("memo(1000) worked")
    except RecursionError as e:
        print("memo(1000) -> RecursionError:", e)
    ways_memo.cache_clear()
    for n in range(0, 1001, 100):      # warm-up bottom-up keeps depth small
        ways_memo(n)
    print("memo(1000) after warming the cache in steps of 100: digits =", len(str(ways_memo(1000))))
    old = sys.getrecursionlimit(); sys.setrecursionlimit(5000)
    ways_memo.cache_clear(); calls = 0
    r = ways_memo(1000)
    print("memo(1000) with recursionlimit 5000: digits =", len(str(r)), "calls =", calls)
    sys.setrecursionlimit(old)
    r_loop = ways_loop(1000)
    print("loop(1000): digits =", len(str(r_loop)), "| equals memo:", r_loop == r)
    print("ways(1000) first 20 digits:", str(r_loop)[:20])

    print("\nTiming (seconds):")
    t = time.perf_counter(); ways_naive(30); print(f"  naive n=30   : {time.perf_counter()-t:.4f}")
    ways_memo.cache_clear(); sys.setrecursionlimit(5000)
    t = time.perf_counter(); ways_memo(1000); print(f"  memo n=1000  : {time.perf_counter()-t:.6f}")
    t = time.perf_counter(); ways_loop(1000); print(f"  loop n=1000  : {time.perf_counter()-t:.6f}")
