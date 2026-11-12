"""B3 - generate clean synthetic data: N stations x 365 days x 24 h (8,760 rows per station)."""
import csv
import os
import random
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data_generated")      # not committed (see .gitignore)


def generate(n_stations, seed=3):
    folder = os.path.join(DATA, f"{n_stations}_stations")
    if os.path.isdir(folder) and len(os.listdir(folder)) == n_stations:
        return folder
    os.makedirs(folder, exist_ok=True)
    rnd = random.Random(seed)
    days = [(date(2026, 1, 1) + timedelta(d)).isoformat() for d in range(365)]
    for s in range(n_stations):
        base = rnd.uniform(40, 100)
        with open(os.path.join(folder, f"S{s:03d}.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["station", "date", "hour", "pm25"])
            for d in days:
                for h in range(24):
                    w.writerow([f"S{s:03d}", d, h, round(base + rnd.gauss(0, 12), 1)])
    return folder


if __name__ == "__main__":
    for n in (1, 12, 120):
        print(n, "stations ->", generate(n))
