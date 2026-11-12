"""B2.1 - feed the cleaning pipeline (B1/cleaning.py) with hostile files. Run: python adversarial_files.py"""
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "B1"))
from cleaning import clean_file

D = os.path.join(here, "data")
os.makedirs(D, exist_ok=True)
HDR = "station,date,hour,pm25,pm10,no2,temperature"
ROWS = ["Adyar,2026-10-01,0,48,90,30,28.5", "Adyar,2026-10-01,1,50,92,31,28.1"]


def w(name, data, enc="utf-8"):
    with open(os.path.join(D, name), "wb") as f:
        f.write(data if isinstance(data, bytes) else data.encode(enc))


w("missing_column.csv", "\n".join(["station,date,hour,pm25,pm10,temperature"] +
                                  [",".join(r.split(",")[:5] + [r.split(",")[6]]) for r in ROWS]) + "\n")
w("semicolon.csv", "\n".join(x.replace(",", ";") for x in [HDR] + ROWS) + "\n")
w("tab.csv", "\n".join(x.replace(",", "\t") for x in [HDR] + ROWS) + "\n")
w("latin1.csv", "\n".join([HDR] + [r.replace("Adyar", "P\u00e9rungudi") for r in ROWS]) + "\n", "cp1252")
w("utf16.csv", "\n".join([HDR] + ROWS) + "\n", "utf-16")
w("empty.csv", b"")
w("header_only.csv", HDR + "\n")

for name in ["missing_column.csv", "semicolon.csv", "tab.csv", "latin1.csv", "utf16.csv",
             "empty.csv", "header_only.csv"]:
    print(f"\n### {name}")
    try:
        rows, rep = clean_file(os.path.join(D, name))
        print("  -> OK, rows kept:", len(rows), "| first row:", rows[0] if rows else None)
    except Exception as e:                     # the program must fail CLEARLY, never crash silently
        print(f"  -> rejected with {type(e).__name__}: {e}")
