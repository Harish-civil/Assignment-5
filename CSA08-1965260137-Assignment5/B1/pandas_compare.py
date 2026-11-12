"""B1 Alternative concept - csv-module loops vs pandas for 1,000 / 100,000 / 1,000,000 rows.
Measures time (perf_counter, best of 3) and peak extra memory (tracemalloc).
Run: python pandas_compare.py
"""
import csv
import io
import random
import time
import tracemalloc

import pandas as pd

random.seed(7)


def make_text(n):
    lines = ["station,date,pm25"]
    for i in range(n):
        r = random.random()
        v = "NA" if r < .03 else "" if r < .05 else str(-random.randint(1, 30)) if r < .07 \
            else "5000" if r < .08 else str(round(random.uniform(20, 200), 1))
        lines.append(f"S{i % 12},2026-10-{i % 28 + 1:02d},{v}")
    return "\n".join(lines) + "\n"


def loop_version(text):
    vals = []
    for rec in csv.DictReader(io.StringIO(text)):
        v = rec["pm25"].strip()
        if v == "" or v.upper() == "NA":
            continue
        f = float(v)
        if f < 0 or f > 999:
            continue
        vals.append(f)
    lo, hi = min(vals), max(vals)
    return [(x - lo) / (hi - lo) for x in vals]


def pandas_version(text):
    df = pd.read_csv(io.StringIO(text), na_values=["NA", ""])
    df = df.dropna(subset=["pm25"])
    df = df[(df.pm25 >= 0) & (df.pm25 <= 999)]
    return ((df.pm25 - df.pm25.min()) / (df.pm25.max() - df.pm25.min())).to_numpy()


def measure(fn, text):
    best = 1e9
    for _ in range(3):
        t0 = time.perf_counter(); res = fn(text); best = min(best, time.perf_counter() - t0)
    tracemalloc.start(); fn(text)
    peak = tracemalloc.get_traced_memory()[1] / 1e6
    tracemalloc.stop()
    return best, peak, len(res)


print(f"{'rows':>10} | {'loop s':>8} {'loop MB':>8} | {'pandas s':>9} {'pandas MB':>9} | speed-up")
for n in (1_000, 100_000, 1_000_000):
    text = make_text(n)
    tl, ml, kl = measure(loop_version, text)
    tp, mp, kp = measure(pandas_version, text)
    assert kl == kp
    print(f"{n:>10,} | {tl:8.4f} {ml:8.1f} | {tp:9.4f} {mp:9.1f} | {tl / tp:5.1f}x")
