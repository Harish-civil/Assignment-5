"""B1.1 - validate the cleaning rules on sample_raw.csv (every problem of A1.1)."""
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from cleaning import clean_text, min_max, z_score

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
here = os.path.dirname(__file__)
text = open(os.path.join(here, "sample_raw.csv")).read()

print("=== BEFORE CLEANING (raw file) ===")
print(text)
rows, rep = clean_text(text)
print("=== AFTER CLEANING ===")
print("station   date        hr  pm25   pm10  no2  temp_c filled")
for r in rows:
    print(f"{r[0]:<9} {r[1]}  {r[2]:>2}  " + "  ".join(
        f"{'NULL' if v is None else v:>5}" for v in r[3:7]) + f"  {r[7]:>3}")
print("\nReport:", rep)

# ---- assertions: one per rule -------------------------------------------------
by = {(r[0], r[1], r[2]): r for r in rows}
assert rep["rows_read"] == 16
assert rep["rejected_row"] == 2                      # bad date + hour 25
assert rep["duplicates"] == 1                        # repeated Adyar hour 3
assert by[("Adyar", "2026-10-01", 1)][3] == 48.0     # 'NA' forward-filled
assert by[("Adyar", "2026-10-01", 2)][3] == 48.0     # blank forward-filled
assert by[("Adyar", "2026-10-01", 4)][3] == 52.0     # negative -> filled
assert by[("Adyar", "2026-10-01", 5)][3] == 52.0     # 1500 -> filled
assert by[("Adyar", "2026-10-01", 5)][4] == 101.0    # 'abc' -> filled
assert ("Guindy", "2026-10-01", 1) in by             # DD/MM/YYYY converted
assert ("Guindy", "2026-10-01", 2) in by             # '  guindy ' -> 'Guindy'
assert by[("Velachery", "2026-10-01", 0)][6] == 29.0 # 84.2 F -> 29.0 C
assert by[("Velachery", "2026-10-01", 2)][6] == 28.5 # NA temp forward-filled
assert by[("Manali", "2026-10-01", 0)][6] is None    # 400 F = 204 C impossible, no previous value
assert min_max([48, 95, 121]) == [0.0, 0.644, 1.0]
assert abs(sum(z_score([48, 95, 121]))) < 1e-9
print("\nAll assertions passed.")
