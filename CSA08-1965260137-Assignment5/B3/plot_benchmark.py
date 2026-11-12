"""Chart of the B3 benchmark (reads outputs/benchmark_output.txt)."""
import os
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

here = os.path.dirname(os.path.abspath(__file__))
rows = [list(map(float, re.sub(",", "", l).split("|")[0].split()[:1] + l.split("|")[1].split()))
        for l in open(os.path.join(here, "outputs", "benchmark_output.txt")) if re.match(r"\s+\d+\s+[\d,]+ \|", l)]
names = ["loops + statistics.mean", "running sum", "pandas groupby", "SQL GROUP BY (query)", "SQL load + query"]
x = list(range(len(rows)))
plt.figure(figsize=(8, 4.5))
for j, n in enumerate(names):
    plt.plot([int(r[0]) for r in rows], [r[1 + j] for r in rows], marker="o", label=n)
plt.xscale("log"); plt.yscale("log"); plt.xticks([1, 12, 120], ["1", "12", "120"])
plt.xlabel("Number of stations (8,760 readings each)"); plt.ylabel("Time (seconds, log scale)")
plt.title("Daily mean PM2.5 per station: time vs data size"); plt.grid(alpha=.3, which="both"); plt.legend()
plt.tight_layout(); plt.savefig(os.path.join(here, "outputs", "benchmark_chart.png"), dpi=130)
print("saved benchmark_chart.png")
