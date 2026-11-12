"""A2 alternative - drop vs forward-fill vs median-fill: effect on the mean and the time (1,000,000 values)."""
import random
import time
import statistics

random.seed(11)
N = 1_000_000
vals = [None if random.random() < 0.05 else round(random.gauss(80, 25) + (i % 24) * .3, 1) for i, _ in enumerate(range(N))]


def drop(v):
    return [x for x in v if x is not None]


def ffill(v):
    out, last = [], None
    for x in v:
        if x is None:
            x = last
        else:
            last = x
        out.append(x)
    return [x for x in out if x is not None]


def median_fill(v):
    med = statistics.median(x for x in v if x is not None)       # sorts: O(n log n)
    return [med if x is None else x for x in v]


print(f"{N:,} values, {sum(x is None for x in vals):,} missing (about 5%)")
print(f"{'strategy':12} {'time s':>8} {'kept':>10} {'mean':>8}")
for name, fn in (("drop", drop), ("forward fill", ffill), ("median fill", median_fill)):
    t0 = time.perf_counter(); r = fn(vals); dt = time.perf_counter() - t0
    print(f"{name:12} {dt:8.3f} {len(r):>10,} {sum(r) / len(r):8.3f}")

# a day where the missing hours are exactly the rush hours (the dangerous case for dropping)
day = [60] * 7 + [None] * 3 + [60] * 7 + [None] * 3 + [60] * 4          # 24 hours
day[7:10] = [None] * 3
true_day = [60] * 7 + [110, 120, 115] + [60] * 7 + [130, 140, 135] + [60] * 4
d = [x for x in day if x is not None]
f, last = [], 60
for x in day:
    last = x if x is not None else last
    f.append(last)
print("\nBiased-gap example (rush hours missing): true mean "
      f"{sum(true_day) / 24:.1f} | drop {sum(d) / len(d):.1f} | forward fill {sum(f) / 24:.1f}")
