"""Generate synthetic RAW station CSV files for October 2026 (12 stations x 31 days x 24 h).
Deliberately injects the faults listed in A1.1. Deterministic (seed 1965260137).
Run:  python generate_data.py
"""
import csv
import os
import random
import math

random.seed(1965260137)
STATIONS = {  # name: (base PM2.5, reports Fahrenheit?)
    "Adyar": 52, "Guindy": 78, "Velachery": 66, "Manali": 92, "Alandur": 58,
    "Anna Nagar": 49, "Kodungaiyur": 97, "Perungudi": 61, "T Nagar": 70,
    "Royapuram": 85, "Sholinganallur": 44, "Ennore": 101,
}
FAHRENHEIT = {"Velachery", "Manali"}
OUT = os.path.join(os.path.dirname(__file__), "data", "raw")
os.makedirs(OUT, exist_ok=True)

for name, base in STATIONS.items():
    rows = []
    for day in range(1, 32):
        day_factor = random.uniform(0.8, 1.25)
        for hour in range(24):
            temp = 27 + 5 * math.sin((hour - 9) / 24 * 2 * math.pi) + random.gauss(0, 0.6)
            rush = 18 * math.exp(-((hour - 8) ** 2) / 6) + 22 * math.exp(-((hour - 20) ** 2) / 8)
            night = 10 if hour < 6 else 0
            pm25 = max(5, base * day_factor + rush + night + random.gauss(0, 5))
            pm10 = pm25 * random.uniform(1.6, 2.0)
            no2 = 20 + 0.25 * pm25 + random.gauss(0, 4)
            if name in FAHRENHEIT:
                temp = temp * 9 / 5 + 32
            vals = [round(pm25, 1), round(pm10, 1), round(max(no2, 1), 1), round(temp, 1)]
            for i in range(4):                      # inject faults
                r = random.random()
                if r < 0.020:
                    vals[i] = random.choice(["", "NA"])
                elif r < 0.028:
                    vals[i] = -round(random.uniform(1, 30), 1)
                elif r < 0.032:
                    vals[i] = 9999
            rows.append([name, f"2026-10-{day:02d}", hour] + vals)
            if random.random() < 0.003:             # duplicate line
                rows.append(rows[-1][:])
    with open(os.path.join(OUT, name.replace(" ", "_") + ".csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["station", "date", "hour", "pm25", "pm10", "no2", "temperature"])
        w.writerows(rows)
print("raw files written to", OUT, "->", len(STATIONS), "stations")
