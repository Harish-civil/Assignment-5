"""B1.3 - clean all raw files, load into SQLite with executemany, answer the three board questions.
Run:  python store_query.py
"""
import glob
import logging
import os
import sqlite3
import time

import pandas as pd
from cleaning import clean_file, FAHRENHEIT_STATIONS

logging.basicConfig(level=logging.WARNING)
here = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(here, "aq.db")
if os.path.exists(DB):
    os.remove(DB)

SCHEMA = """
CREATE TABLE stations (
    station_id   INTEGER PRIMARY KEY,
    name         TEXT NOT NULL UNIQUE,
    raw_temp_unit TEXT NOT NULL CHECK (raw_temp_unit IN ('C','F'))
);
CREATE TABLE readings (
    reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_id INTEGER NOT NULL REFERENCES stations(station_id),
    day        TEXT    NOT NULL,            -- YYYY-MM-DD
    hour       INTEGER NOT NULL CHECK (hour BETWEEN 0 AND 23),
    pm25 REAL, pm10 REAL, no2 REAL, temp_c REAL,
    filled     INTEGER NOT NULL DEFAULT 0,  -- how many fields were forward-filled
    UNIQUE (station_id, day, hour)
);
"""

con = sqlite3.connect(DB)
con.executescript(SCHEMA)

totals = {}
all_rows = []
for path in sorted(glob.glob(os.path.join(here, "data", "raw", "*.csv"))):
    rows, rep = clean_file(path)
    for k, v in rep.items():
        totals[k] = totals.get(k, 0) + v
    all_rows.extend(rows)

names = sorted({r[0] for r in all_rows})
con.executemany("INSERT INTO stations(name, raw_temp_unit) VALUES (?, ?)",
                [(n, "F" if n in FAHRENHEIT_STATIONS else "C") for n in names])
ids = dict(con.execute("SELECT name, station_id FROM stations"))
t0 = time.perf_counter()
con.executemany(
    "INSERT INTO readings(station_id, day, hour, pm25, pm10, no2, temp_c, filled) "
    "VALUES (?,?,?,?,?,?,?,?)",
    [(ids[r[0]], r[1], r[2], r[3], r[4], r[5], r[6], r[7]) for r in all_rows])
con.commit()
print(f"Loaded {len(all_rows)} cleaned rows with ONE executemany in "
      f"{(time.perf_counter() - t0) * 1000:.1f} ms")
print("Cleaning totals over 12 files:", totals)

print("\n--- Q1: average PM2.5 of Adyar in October 2026 ---")
sql1 = """SELECT ROUND(AVG(r.pm25), 2) FROM readings r JOIN stations s USING(station_id)
          WHERE s.name = ? AND r.day BETWEEN '2026-10-01' AND '2026-10-31'"""
print(con.execute(sql1, ("Adyar",)).fetchone()[0])

print("\n--- Q2: stations ranked by October mean PM2.5 ---")
sql2 = """SELECT s.name, ROUND(AVG(r.pm25),2) AS mean_pm25, COUNT(r.pm25) AS n_valid
          FROM readings r JOIN stations s USING(station_id)
          GROUP BY s.name ORDER BY mean_pm25 DESC"""
for row in con.execute(sql2):
    print(f"{row[0]:<15}{row[1]:>8}{row[2]:>8}")

print("\n--- Q3: the five hours of the day with the worst air (all stations) ---")
sql3 = """SELECT hour, ROUND(AVG(pm25),2) AS mean_pm25 FROM readings
          GROUP BY hour ORDER BY mean_pm25 DESC LIMIT 5"""
for row in con.execute(sql3):
    print(f"hour {row[0]:>2}:00  {row[1]}")

# --- same Q1 answered by reading the CSV files with pandas (A1.3 comparison) ---------
t0 = time.perf_counter()
df = pd.read_csv(os.path.join(here, "data", "raw", "Adyar.csv"), na_values=["NA", ""])
df = df[(df.pm25 >= 0) & (df.pm25 <= 999)]
csv_ans = round(df.pm25.mean(), 2)
t_csv = (time.perf_counter() - t0) * 1000
t0 = time.perf_counter()
con.execute(sql1, ("Adyar",)).fetchone()
t_sql = (time.perf_counter() - t0) * 1000
print(f"\nQ1 via pandas on raw CSV (no forward fill): {csv_ans}  ({t_csv:.2f} ms)")
print(f"Q1 via SQL on cleaned table              : {t_sql:.2f} ms")
con.close()
