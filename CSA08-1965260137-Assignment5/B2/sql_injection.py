"""B2.2 - station name with a quote: string concatenation vs ? placeholder."""
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)")
con.executemany("INSERT INTO aq VALUES (?,?,?)", [
    ("Adyar", "2026-10-01", 48.0), ("Guindy", "2026-10-01", 95.0),
    ("O'Brien Road", "2026-10-01", 70.0), ("Ennore", "2026-10-01", 120.0)])


def unsafe(name):
    sql = "SELECT AVG(pm25) FROM aq WHERE station = '" + name + "'"
    print("   SQL sent:", sql)
    try:
        return con.execute(sql).fetchone()[0]
    except sqlite3.Error as e:
        return f"ERROR {type(e).__name__}: {e}"


def safe(name):
    return con.execute("SELECT AVG(pm25) FROM aq WHERE station = ?", (name,)).fetchone()[0]


for name in ["Adyar", "O'Brien Road", "Adyar' OR '1'='1", "x'; DROP TABLE aq; --"]:
    print(f"\nInput: {name!r}")
    print("  concatenation ->", unsafe(name))
    print("  ? placeholder ->", safe(name))

print("\nTable still exists?", con.execute("SELECT COUNT(*) FROM aq").fetchone()[0], "rows")
print("(sqlite3.execute() refuses to run two statements in one call, so DROP TABLE could not run here, "
      "but other databases / executescript() do allow stacked queries.)")
