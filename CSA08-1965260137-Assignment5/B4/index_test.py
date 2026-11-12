"""B4.2 - effect of an index on (station, day) at the NEW scale:
112 stations x 30 days x 96 readings (every 15 minutes) = 322,560 rows."""
import random
import sqlite3
import time

random.seed(5)
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE aq (station TEXT, day TEXT, slot INTEGER, pm25 REAL)")
rows = [(f"ST{s:03d}", f"2026-10-{d:02d}", q, round(random.uniform(20, 200), 1))
        for s in range(112) for d in range(1, 31) for q in range(96)]
t0 = time.perf_counter()
con.executemany("INSERT INTO aq VALUES (?,?,?,?)", rows)
con.commit()
print(f"rows: {len(rows):,}  loaded (no index) in {time.perf_counter() - t0:.2f} s")

Q_DAY = "SELECT AVG(pm25) FROM aq WHERE station = ? AND day = ?"
Q_SUMMARY = ("SELECT day, MIN(pm25), MAX(pm25), AVG(pm25), COUNT(pm25) FROM aq "
             "WHERE station = ? GROUP BY day")


def bench(sql, reps, params_fn):
    t0 = time.perf_counter()
    for i in range(reps):
        con.execute(sql, params_fn(i)).fetchall()
    return (time.perf_counter() - t0) / reps * 1000


for name, sql, reps, pf in (
        ("avg of one station, one day", Q_DAY, 100, lambda i: (f"ST{i % 112:03d}", "2026-10-15")),
        ("daily summary of one station", Q_SUMMARY, 100, lambda i: (f"ST{i % 112:03d}",))):
    print(f"\n{name}")
    print("  plan before:", con.execute("EXPLAIN QUERY PLAN " + sql, pf(0)).fetchall()[0][-1])
    before = bench(sql, reps, pf)
    if not con.execute("SELECT 1 FROM sqlite_master WHERE name='idx_station_day'").fetchone():
        t0 = time.perf_counter()
        con.execute("CREATE INDEX idx_station_day ON aq(station, day)")
        build = time.perf_counter() - t0
    print("  plan after :", con.execute("EXPLAIN QUERY PLAN " + sql, pf(0)).fetchall()[0][-1])
    after = bench(sql, reps, pf)
    print(f"  no index {before:8.3f} ms/query | with index {after:8.3f} ms/query | speed-up {before / after:6.1f}x")
    con.execute("DROP INDEX idx_station_day")
con.execute("CREATE INDEX idx_station_day ON aq(station, day)")
print(f"\nindex build time: {build:.3f} s")
t0 = time.perf_counter()
con.executemany("INSERT INTO aq VALUES (?,?,?,?)", [("ST999", "2026-11-01", q, 50.0) for q in range(10000)])
print(f"insert of 10,000 rows WITH index: {time.perf_counter() - t0:.3f} s")
