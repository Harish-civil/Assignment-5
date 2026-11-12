"""Q4 - += vs join() vs f-string vs StringIO. Author: M Ayaan (1965260137) | CSA0809"""
import time, io, statistics, csv

def lines(n):
    return [f"Item{i}:Rs{i % 50}" for i in range(n)]

def build_plus(parts):
    text = ""
    for p in parts:
        text += p + ";"
    return text

def build_join(parts):
    return ";".join(parts) + ";" if parts else ""            # TODO 1 (single join)

def build_fstring_plus(n):
    text = ""
    for i in range(n):
        text += f"Item{i}:Rs{i % 50};"
    return text

def build_fstring_join(n):
    return "".join([f"Item{i}:Rs{i % 50};" for i in range(n)])

def build_stringio(parts):
    buf = io.StringIO()
    for p in parts:
        buf.write(p); buf.write(";")
    return buf.getvalue()

def build_plus_defeated(parts):
    """+= with a second reference alive, so CPython cannot resize in place."""
    text = ""
    keep = None
    for p in parts:
        keep = text                  # extra reference -> refcount > 1 -> copy every time
        text += p + ";"
    return text

def timeit(fn, *a, repeat=3):
    ts = []
    for _ in range(repeat):
        t = time.perf_counter(); r = fn(*a); ts.append(time.perf_counter() - t)
    return statistics.mean(ts), ts, r

if __name__ == "__main__":
    items = [f"Item{i}:Rs{i % 50}" for i in range(200_000)]
    start = time.perf_counter(); a = build_plus(items); t_plus = time.perf_counter() - start
    start = time.perf_counter(); b = build_join(items); t_join = time.perf_counter() - start
    print("same text:", a == b, "| length:", len(b))
    print(f"+= time: {t_plus:.4f} s join time: {t_join:.4f} s")

    print("\nThree runs of the Complete-the-Code program (200,000 items):")
    rp, rj = [], []
    for k in range(3):
        _, tp, _ = timeit(build_plus, items, repeat=1); _, tj, _ = timeit(build_join, items, repeat=1)
        rp += tp; rj += tj
        print(f"  run {k+1}: += {tp[0]:.4f} s | join {tj[0]:.4f} s")
    print(f"  average: += {statistics.mean(rp):.4f} s | join {statistics.mean(rj):.4f} s")

    print("\nMeasured times (mean of 3 runs, seconds):")
    header = ["lines", "plus_eq", "join", "fstring_plus_eq", "fstring_join", "stringio", "plus_eq_defeated"]
    rows = []
    for n in (1_000, 10_000, 200_000):
        parts = lines(n)
        row = [n]
        for fn, arg in [(build_plus, parts), (build_join, parts), (build_fstring_plus, n),
                        (build_fstring_join, n), (build_stringio, parts)]:
            row.append(round(timeit(fn, arg)[0], 5))
        # the defeated version is O(n^2): use 1 repeat and cap very large size
        row.append(round(timeit(build_plus_defeated, parts, repeat=1 if n > 10_000 else 3)[0], 5))
        rows.append(row)
    print(" | ".join(f"{h:>16}" for h in header))
    for r in rows:
        print(" | ".join(f"{x:>16}" for x in r))
    with open("q4_timings.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)

    print("\nGrowth check of plain += (time ratio when n grows x10):")
    for i in range(1, 3):
        print(f"  n {rows[i-1][0]} -> {rows[i][0]}: ratio = {rows[i][1]/rows[i-1][1]:.1f}")
    print("Growth check of defeated += (O(n^2) expected -> about x100 per x10):")
    for i in range(1, 3):
        print(f"  n {rows[i-1][0]} -> {rows[i][0]}: ratio = {rows[i][6]/rows[i-1][6]:.1f}")
