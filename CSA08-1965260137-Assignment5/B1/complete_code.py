"""B1 - Complete the Code (TODO 1 and TODO 2) + extra check for pm25 > 999 and a test row."""
import csv
import io

RAW = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
"""

# extra test row for the new rule (pm25 above 999 must be skipped)
RAW_WITH_FAULT = RAW + "Guindy,2026-10-04,5000\n"


def load_clean(text):
    """Returns (station, date, pm25) tuples for valid, non-negative readings only."""
    rows = []
    for rec in csv.DictReader(io.StringIO(text)):
        value = rec["pm25"].strip()
        if value == "" or value.upper() == "NA":
            continue
        pm = float(value)
        if pm < 0 or pm > 999:          # added check: negative or impossibly large
            continue
        rows.append((rec["station"], rec["date"], pm))
    return rows


def min_max(values):
    lo, hi = min(values), max(values)
    return [round((v - lo) / (hi - lo), 3) for v in values]


clean = load_clean(RAW)
print(clean)
print(min_max([pm for _, _, pm in clean]))

# test of the extra check
extra = load_clean(RAW_WITH_FAULT)
assert extra == clean, "row with pm25 = 5000 must be skipped"
print("Extra test passed: pm25 = 5000 row was skipped ->", len(extra), "rows kept")
