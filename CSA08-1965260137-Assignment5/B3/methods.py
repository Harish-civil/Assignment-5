"""B3 - the three ways to compute the daily mean PM2.5 per station, plus the running-sum alternative."""
import csv
import glob
import os
import sqlite3
import statistics
from collections import defaultdict

import pandas as pd


def files(folder):
    return sorted(glob.glob(os.path.join(folder, "*.csv")))


# ---- Method 1: plain Python loops, store all readings, statistics.mean -------------------
def loops_store_all(folder):
    groups = defaultdict(list)
    for path in files(folder):
        with open(path, newline="") as f:
            for rec in csv.DictReader(f):
                groups[(rec["station"], rec["date"])].append(float(rec["pm25"]))
    return {k: statistics.mean(v) for k, v in groups.items()}


# ---- Alternative: one pass, running sum and count --------------------------------------
def loops_running_sum(folder):
    tot, cnt = defaultdict(float), defaultdict(int)
    for path in files(folder):
        with open(path, newline="") as f:
            reader = csv.reader(f)
            next(reader)
            for station, day, _hour, pm in reader:
                k = (station, day)
                tot[k] += float(pm)
                cnt[k] += 1
    return {k: tot[k] / cnt[k] for k in tot}


# ---- Method 2: pandas -------------------------------------------------------------------
def pandas_groupby(folder):
    df = pd.concat((pd.read_csv(p) for p in files(folder)), ignore_index=True)
    g = df.groupby(["station", "date"])["pm25"].mean()
    return g.to_dict()


# ---- Method 3: SQL ----------------------------------------------------------------------
def build_db(folder):
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE aq (station TEXT, day TEXT, hour INTEGER, pm25 REAL)")
    for path in files(folder):
        with open(path, newline="") as f:
            reader = csv.reader(f)
            next(reader)
            con.executemany("INSERT INTO aq VALUES (?,?,?,?)",
                            ((s, d, int(h), float(p)) for s, d, h, p in reader))
    con.commit()
    return con


def sql_query(con):
    rows = con.execute("SELECT station, day, AVG(pm25) FROM aq GROUP BY station, day")
    return {(s, d): m for s, d, m in rows}


def sql_load_and_query(folder):
    con = build_db(folder)
    res = sql_query(con)
    con.close()
    return res
