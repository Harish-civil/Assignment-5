"""B2 Alternative concept - executemany() vs execute() in a loop, and fresh commit per row."""
import os
import sqlite3
import tempfile
import time


def run(mode, n, path=":memory:"):
    con = sqlite3.connect(path)
    con.execute("CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)")
    data = [(f"S{i % 12}", "2026-10-01", float(i % 200)) for i in range(n)]
    t0 = time.perf_counter()
    if mode == "executemany":
        con.executemany("INSERT INTO aq VALUES (?,?,?)", data)
        con.commit()
    elif mode == "execute loop":
        for r in data:
            con.execute("INSERT INTO aq VALUES (?,?,?)", r)
        con.commit()
    else:                                       # commit after every row (worst case, on disk)
        for r in data:
            con.execute("INSERT INTO aq VALUES (?,?,?)", r)
            con.commit()
    dt = time.perf_counter() - t0
    con.close()
    return dt


print(f"{'rows':>9} | {'executemany':>12} | {'execute loop':>12} | {'commit/row (disk)':>18}")
for n in (1_000, 10_000, 100_000, 500_000):
    a, b = run("executemany", n), run("execute loop", n)
    if n <= 1_000:
        f = os.path.join(tempfile.mkdtemp(), "t.db")
        c = f"{run('commit each', n, f):18.3f}"
    else:
        c = f"{'(skipped)':>18}"
    print(f"{n:>9,} | {a:12.4f} | {b:12.4f} | {c}")
