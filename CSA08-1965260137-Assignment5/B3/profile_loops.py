"""B3.3 - cProfile of the plain-Python version (12 stations)."""
import cProfile
import io
import pstats

from make_data import generate
from methods import loops_store_all

folder = generate(12)
pr = cProfile.Profile()
pr.enable()
loops_store_all(folder)
pr.disable()
s = io.StringIO()
pstats.Stats(pr, stream=s).sort_stats("tottime").print_stats(8)
print(s.getvalue())
s = io.StringIO()
pstats.Stats(pr, stream=s).sort_stats("cumulative").print_stats(6)
print(s.getvalue())
