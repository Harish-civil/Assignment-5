"""Q1 - Electricity subsidy: separate ifs vs if-elif-else, plus alternatives.
Author: M Ayaan (1965260137) | CSA0809 Python Programming"""
import time

# ---------- (A) separate if statements (the developer's buggy style) ----------
def subsidy_separate(units, ration_card, member_above_80):
    result = []
    if units <= 100:
        result.append("FULL")
    if units <= 200 and ration_card:          # missing lower bound -> overlaps the first rule
        result.append("PARTIAL")
    if units > 200 and member_above_80:
        result.append("FULL(80+)")
    if not result:
        result.append("NONE")
    return result

# ---------- (B) if-elif-else: exactly one branch can run ----------
def subsidy_elif(units, ration_card, member_above_80):
    if units <= 100:
        return "FULL"
    elif 101 <= units <= 200:
        return "PARTIAL" if ration_card else "NONE"
    else:
        return "FULL(80+)" if member_above_80 else "NONE"

# ---------- Design decision: combined Boolean conditions (flat) ----------
def subsidy_boolean(units, ration_card, member_above_80):
    if units <= 100:
        return "FULL"
    if 101 <= units <= 200 and ration_card:
        return "PARTIAL"
    if units > 200 and member_above_80:
        return "FULL(80+)"
    return "NONE"

# ---------- Alternative 1: slab table searched in a loop ----------
SLABS = [(100, "FULL"), (200, "PARTIAL?"), (float("inf"), "ELDER?")]
def subsidy_table(units, ration_card, member_above_80):
    for upper, rule in SLABS:
        if units <= upper:
            if rule == "FULL":
                return "FULL"
            if rule == "PARTIAL?":
                return "PARTIAL" if ration_card else "NONE"
            return "FULL(80+)" if member_above_80 else "NONE"

# ---------- Alternative 2: match-case (Python 3.10+) ----------
def subsidy_match(units, ration_card, member_above_80):
    match units:
        case u if u <= 100:
            return "FULL"
        case u if u <= 200:
            return "PARTIAL" if ration_card else "NONE"
        case _:
            return "FULL(80+)" if member_above_80 else "NONE"

# ---------- Eight households: (units, ration card, member above 80) ----------
HOUSEHOLDS = [
    (0,   False, False),
    (100, True,  False),   # boundary, has ration card (exposes double result)
    (101, True,  False),   # boundary
    (101, False, False),
    (200, True,  False),   # boundary
    (200, False, True),    # boundary, 80+ irrelevant in this slab
    (201, False, True),    # boundary
    (201, True,  False),
]

# predictions written BEFORE running (see report)
PREDICTED = ["FULL", "FULL", "PARTIAL", "NONE", "PARTIAL", "NONE", "FULL(80+)", "NONE"]

if __name__ == "__main__":
    print(f"{'units':>5} {'ration':>6} {'80+':>5} | {'predicted':<10} {'if-elif':<10} {'separate-if':<16} {'boolean':<10} {'table':<10} {'match':<10}")
    for (u, r, e), p in zip(HOUSEHOLDS, PREDICTED):
        print(f"{u:>5} {str(r):>6} {str(e):>5} | {p:<10} {subsidy_elif(u,r,e):<10} "
              f"{'+'.join(subsidy_separate(u,r,e)):<16} {subsidy_boolean(u,r,e):<10} "
              f"{subsidy_table(u,r,e):<10} {subsidy_match(u,r,e):<10}")

    mismatch = 0
    for u in range(0, 401):
        for r in (False, True):
            for e in (False, True):
                a = subsidy_elif(u, r, e)
                if not (a == subsidy_boolean(u, r, e) == subsidy_table(u, r, e) == subsidy_match(u, r, e)):
                    mismatch += 1
    print("\nmismatches among correct versions over 1604 inputs:", mismatch)

    dup = sum(1 for u in range(0, 401) for r in (False, True) for e in (False, True)
              if len(subsidy_separate(u, r, e)) > 1)
    print("inputs with more than one result (separate ifs):", dup)

    print("\nTime per decision (microseconds), 200000 calls, worst-case last slab:")
    N = 200_000
    for name, fn in [("if-elif", subsidy_elif), ("table-loop", subsidy_table), ("match-case", subsidy_match)]:
        t = time.perf_counter()
        for _ in range(N):
            fn(250, False, True)
        print(f"  {name:<11}: {(time.perf_counter()-t)/N*1e6:.3f} us")

    print("\nSlab-table lookup vs k (worst case = last slab), 100000 lookups:")
    for k in (3, 10, 100, 1000):
        table = [(i * 10, f"D{i}") for i in range(k)]
        probe = (k - 1) * 10
        t = time.perf_counter()
        for _ in range(100_000):
            for upper, d in table:
                if probe <= upper:
                    break
        print(f"  k={k:<5} {(time.perf_counter()-t)/100_000*1e6:.3f} us per decision")
