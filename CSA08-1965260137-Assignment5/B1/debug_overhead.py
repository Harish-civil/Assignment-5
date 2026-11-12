"""A4 alternative - cost of print() vs logging (enabled / disabled) for 200,000 calls, written to a file."""
import logging
import os
import sys
import tempfile
import time

N = 200_000
tmp = tempfile.mkdtemp()


def t_print():
    f = open(os.path.join(tmp, "p.txt"), "w")
    t0 = time.perf_counter()
    for i in range(N):
        print("row", i, "value", i * 1.5, file=f)
    f.close()
    return time.perf_counter() - t0


def t_logging(level):
    lg = logging.getLogger(f"x{level}")
    lg.handlers.clear(); lg.propagate = False
    h = logging.FileHandler(os.path.join(tmp, f"l{level}.txt")); lg.addHandler(h); lg.setLevel(level)
    t0 = time.perf_counter()
    for i in range(N):
        lg.debug("row %d value %s", i, i * 1.5)
    h.close()
    return time.perf_counter() - t0


def t_none():
    t0 = time.perf_counter()
    for i in range(N):
        pass
    return time.perf_counter() - t0


print(f"{N:,} debug messages")
print(f"  empty loop (baseline)            : {t_none():.4f} s")
print(f"  print() to file                  : {t_print():.4f} s")
print(f"  logging.debug, level DEBUG (on)  : {t_logging(logging.DEBUG):.4f} s")
print(f"  logging.debug, level INFO (off)  : {t_logging(logging.INFO):.4f} s")
