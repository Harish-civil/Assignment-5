"""B3.1 - small data: do the three methods agree?  (3 stations x 365 days -> restricted to Jan 1-7)"""
import os
import tempfile
import csv

from methods import loops_store_all, loops_running_sum, pandas_groupby, build_db, sql_query
from make_data import generate

src = generate(12)
tmp = tempfile.mkdtemp()
for name in ("S000.csv", "S001.csv", "S002.csv"):
    with open(os.path.join(src, name)) as fin, open(os.path.join(tmp, name), "w", newline="") as fout:
        r = csv.reader(fin); w = csv.writer(fout)
        w.writerow(next(r))
        w.writerows(row for row in r if row[1] <= "2026-01-07")

a, b, c, d = (loops_store_all(tmp), pandas_groupby(tmp), sql_query(build_db(tmp)), loops_running_sum(tmp))
print("groups (station, day):", len(a), len(b), len(c), len(d))
assert a.keys() == b.keys() == c.keys() == d.keys()
worst = max(max(abs(a[k] - b[k]), abs(a[k] - c[k]), abs(a[k] - d[k])) for k in a)
print(f"largest difference between methods: {worst:.2e}")
assert worst < 1e-9
for k in sorted(a)[:4]:
    print(k, f"loops={a[k]:.4f}  pandas={b[k]:.4f}  sql={c[k]:.4f}  running-sum={d[k]:.4f}")
print("All methods agree.")
