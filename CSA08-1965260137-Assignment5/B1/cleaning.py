"""B1 - Cleaning pipeline for the City Air-Quality Monitoring Network.

Implements the rules designed in Part A (A2):
  * station names   -> stripped, Title Case
  * dates           -> ISO 8601 (YYYY-MM-DD); DD/MM/YYYY is accepted and converted
  * missing values  -> '', 'NA', 'N/A', 'NaN', 'null', non-numeric text  => None
  * impossible      -> pollutant < 0 or > 999 ; temperature outside 5..50 C (after conversion)  => None
  * fill rule       -> forward fill per station (max 3 consecutive hours), else stay NULL
  * duplicates      -> same (station, date, hour): first one is kept
  * Fahrenheit      -> stations in FAHRENHEIT_STATIONS are converted: C = (F - 32) * 5 / 9
"""
import csv
import io
import logging
from datetime import datetime

log = logging.getLogger("cleaning")

FAHRENHEIT_STATIONS = {"Velachery", "Manali"}
MISSING_TOKENS = {"", "NA", "N/A", "NAN", "NULL", "NONE", "-"}
POLLUTANT_RANGE = (0.0, 999.0)
TEMP_RANGE_C = (5.0, 50.0)
MAX_FILL_GAP = 3
REQUIRED = ["station", "date", "hour", "pm25", "pm10", "no2", "temperature"]
VALUE_COLS = ["pm25", "pm10", "no2", "temperature"]


def parse_number(text):
    """Return float or None (missing / not a number)."""
    text = (text or "").strip()
    if text.upper() in MISSING_TOKENS:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def parse_date(text):
    text = (text or "").strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return None


def clean_station(name):
    return " ".join((name or "").split()).title()


def clean_text(text, max_gap=MAX_FILL_GAP, fahrenheit=FAHRENHEIT_STATIONS):
    """Clean CSV text. Returns (rows, report).

    rows   : list of (station, date, hour, pm25, pm10, no2, temp_c, filled)
    report : dict of counters
    """
    rep = dict(rows_read=0, rejected_row=0, duplicates=0, missing=0,
               impossible=0, f_to_c=0, filled=0, still_null=0, kept=0)
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None:
        raise ValueError("empty file: no header row")
    header = [h.strip().lower() for h in reader.fieldnames]
    missing_cols = [c for c in REQUIRED if c not in header]
    if missing_cols:
        raise ValueError(f"missing column(s): {missing_cols}")
    reader.fieldnames = header

    seen, parsed = set(), []
    for raw in reader:
        rep["rows_read"] += 1
        station = clean_station(raw["station"])
        day = parse_date(raw["date"])
        try:
            hour = int(float(raw["hour"]))
        except (TypeError, ValueError):
            hour = -1
        if not station or day is None or not 0 <= hour <= 23:
            rep["rejected_row"] += 1
            log.debug("rejected row %r", raw)
            continue
        key = (station, day, hour)
        if key in seen:
            rep["duplicates"] += 1
            continue
        seen.add(key)

        vals = {}
        for col in VALUE_COLS:
            v = parse_number(raw[col])
            if v is None:
                rep["missing"] += 1
            elif col == "temperature":
                if station in fahrenheit:
                    v = round((v - 32) * 5 / 9, 1)
                    rep["f_to_c"] += 1
                lo, hi = TEMP_RANGE_C
                if not lo <= v <= hi:
                    rep["impossible"] += 1
                    v = None
            else:
                lo, hi = POLLUTANT_RANGE
                if not lo <= v <= hi:
                    rep["impossible"] += 1
                    v = None
            vals[col] = v
        parsed.append([station, day, hour, vals])

    # forward fill, per station, in time order
    parsed.sort(key=lambda r: (r[0], r[1], r[2]))
    last, gap, cur_station = {}, {}, None
    out = []
    for station, day, hour, vals in parsed:
        if station != cur_station:
            cur_station, last, gap = station, {}, {c: 0 for c in VALUE_COLS}
        filled = 0
        for col in VALUE_COLS:
            if vals[col] is not None:
                last[col], gap[col] = vals[col], 0
            else:
                gap[col] += 1
                if col in last and gap[col] <= max_gap:
                    vals[col] = last[col]
                    filled += 1
                    rep["filled"] += 1
                else:
                    rep["still_null"] += 1
        out.append((station, day, hour, vals["pm25"], vals["pm10"],
                    vals["no2"], vals["temperature"], filled))
    rep["kept"] = len(out)
    log.info("cleaning report: %s", rep)
    return out, rep


def read_file_text(path):
    """Read a file trying several encodings; normalise the delimiter to a comma."""
    data = open(path, "rb").read()
    if not data.strip():
        raise ValueError("empty file")
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            text = data.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    first = text.splitlines()[0]
    if "," not in first:
        try:
            dialect = csv.Sniffer().sniff(first, delimiters=";\t|")
        except csv.Error:
            raise ValueError("cannot detect the delimiter")
        rows = list(csv.reader(io.StringIO(text), dialect))
        buf = io.StringIO()
        csv.writer(buf, lineterminator="\n").writerows(rows)
        text = buf.getvalue()
    return text


def clean_file(path, **kw):
    return clean_text(read_file_text(path), **kw)


def min_max(values):
    lo, hi = min(values), max(values)
    if hi == lo:
        return [0.0 for _ in values]
    return [round((v - lo) / (hi - lo), 3) for v in values]


def z_score(values):
    n = len(values)
    mean = sum(values) / n
    sd = (sum((v - mean) ** 2 for v in values) / n) ** 0.5
    if sd == 0:
        return [0.0 for _ in values]
    return [round((v - mean) / sd, 3) for v in values]
