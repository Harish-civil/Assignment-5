"""B1.4 - charts designed in A3.1, read from the SQLite database. Run: python visualise.py"""
import os
import sqlite3

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, "outputs")
con = sqlite3.connect(os.path.join(here, "aq.db"))
df = pd.read_sql("SELECT s.name AS station, r.day, r.hour, r.pm25, r.temp_c "
                 "FROM readings r JOIN stations s USING(station_id)", con)
stats = []

# 1. Trend of PM2.5 over a month - LINE
d = df[df.station == "Adyar"].groupby("day").pm25.mean()
plt.figure(figsize=(9, 4))
plt.plot(range(1, len(d) + 1), d.values, marker="o", color="tab:blue")
plt.axhline(60, ls="--", color="red", label="24-h guideline 60 ug/m3")
plt.xlabel("Day of October 2026"); plt.ylabel("Daily mean PM2.5 (ug/m3)")
plt.title("Adyar: daily mean PM2.5, October 2026"); plt.legend(); plt.grid(alpha=.3)
plt.tight_layout(); plt.savefig(os.path.join(out, "chart1_trend_line.png"), dpi=130); plt.close()
stats.append(f"Chart1 Adyar daily mean: min {d.min():.1f} (day {d.idxmin()[-2:]}), "
             f"max {d.max():.1f} (day {d.idxmax()[-2:]}), days above 60: {(d > 60).sum()} of {len(d)}")

# 2. Comparison of stations - BAR (mean) and BOX (spread)
m = df.groupby("station").pm25.mean().sort_values()
plt.figure(figsize=(9, 4.5))
plt.barh(m.index, m.values, color="tab:orange")
plt.xlabel("Mean PM2.5 (ug/m3)"); plt.ylabel("Station")
plt.title("Mean PM2.5 by station, October 2026"); plt.grid(axis="x", alpha=.3)
plt.tight_layout(); plt.savefig(os.path.join(out, "chart2_station_bar.png"), dpi=130); plt.close()
stats.append(f"Chart2 highest {m.index[-1]} {m.iloc[-1]:.1f}; lowest {m.index[0]} {m.iloc[0]:.1f}; "
             f"ratio {m.iloc[-1] / m.iloc[0]:.2f}x")

order = list(m.index)
plt.figure(figsize=(10, 4.5))
plt.boxplot([df[df.station == s].pm25.dropna() for s in order], tick_labels=order)
plt.xticks(rotation=45, ha="right"); plt.ylabel("PM2.5 (ug/m3)"); plt.xlabel("Station")
plt.title("Spread of hourly PM2.5 by station"); plt.tight_layout()
plt.savefig(os.path.join(out, "chart3_station_box.png"), dpi=130); plt.close()

# 3. Temperature vs PM2.5 - SCATTER
s = df.dropna(subset=["pm25", "temp_c"]).sample(1500, random_state=1)
r = df[["pm25", "temp_c"]].corr().iloc[0, 1]
plt.figure(figsize=(7, 5))
plt.scatter(s.temp_c, s.pm25, s=8, alpha=.4)
plt.xlabel("Temperature (deg C)"); plt.ylabel("PM2.5 (ug/m3)")
plt.title(f"Temperature vs PM2.5 (1,500 random readings, r = {r:.2f})"); plt.grid(alpha=.3)
plt.tight_layout(); plt.savefig(os.path.join(out, "chart4_scatter.png"), dpi=130); plt.close()
stats.append(f"Chart4 Pearson r(temp, PM2.5) = {r:.3f}")

# 4. Hours with the worst air - BAR by hour
h = df.groupby("hour").pm25.mean()
colors = ["tab:red" if v >= h.nlargest(4).min() else "tab:gray" for v in h.values]
plt.figure(figsize=(9, 4))
plt.bar(h.index, h.values, color=colors)
plt.xlabel("Hour of day"); plt.ylabel("Mean PM2.5 (ug/m3)"); plt.xticks(range(0, 24, 2))
plt.title("Mean PM2.5 by hour of day (all stations)"); plt.grid(axis="y", alpha=.3)
plt.tight_layout(); plt.savefig(os.path.join(out, "chart5_hours_bar.png"), dpi=130); plt.close()
stats.append(f"Chart5 worst hours: {list(h.nlargest(4).index)}; best hour {h.idxmin()} ({h.min():.1f})")

# 5. Histogram of readings
plt.figure(figsize=(7, 4))
plt.hist(df.pm25.dropna(), bins=40, color="tab:green", edgecolor="white")
plt.xlabel("PM2.5 (ug/m3)"); plt.ylabel("Number of readings")
plt.title("Distribution of PM2.5 readings (all stations)"); plt.tight_layout()
plt.savefig(os.path.join(out, "chart6_hist.png"), dpi=130); plt.close()
stats.append(f"Chart6 mean {df.pm25.mean():.1f}, median {df.pm25.median():.1f}, "
             f"skew {df.pm25.skew():.2f}")

open(os.path.join(out, "chart_stats.txt"), "w").write("\n".join(stats))
print("\n".join(stats))
