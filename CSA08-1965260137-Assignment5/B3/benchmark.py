"""B3.2 - time of every method for 1, 12 and 120 stations (best of 3); memory with tracemalloc."""
import time
import tracemalloc

from make_data import generate
from methods import (loops_store_all, loops_running_sum, pandas_groupby, build_db,
                     sql_query, sql_load_and_query)


def best_time(fn, reps=3):
    best = 1e9
    for _ in range(reps):
        t0 = time.perf_counter(); fn(); best = min(best, time.perf_counter() - t0)
    return best


def peak_mb(fn):
    tracemalloc.start(); fn()
    p = tracemalloc.get_traced_memory()[1] / 1e6
    tracemalloc.stop()
    return p


print(f"{'stations':>8} {'rows':>10} | {'loops':>8} {'run-sum':>8} {'pandas':>8} {'SQL q':>8} {'SQL load+q':>10}   (seconds)")
mem = []
for n in (1, 12, 120):
    folder = generate(n)
    con = build_db(folder)
    t = [best_time(lambda: loops_store_all(folder)), best_time(lambda: loops_running_sum(folder)),
         best_time(lambda: pandas_groupby(folder)), best_time(lambda: sql_query(con)),
         best_time(lambda: sql_load_and_query(folder), reps=2)]
    print(f"{n:>8} {n * 8760:>10,} | " + " ".join(f"{x:8.3f}" for x in t[:4]) + f" {t[4]:10.3f}")
    mem.append((n, peak_mb(lambda: loops_store_all(folder)), peak_mb(lambda: loops_running_sum(folder)),
                peak_mb(lambda: pandas_groupby(folder))))
    con.close()

print("\nPeak Python memory (tracemalloc, MB)")
print(f"{'stations':>8} | {'store-all+mean':>14} {'running-sum':>12} {'pandas':>8}")
for n, a, b, c in mem:
    print(f"{n:>8} | {a:14.1f} {b:12.1f} {c:8.1f}")
