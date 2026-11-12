"""Q3 - Vehicle registration validator (no regex in the main solution).
Author: M Ayaan (1965260137) | CSA0809"""
import re, time

def normalise(text):
    """'tn 09 ab 1234' -> 'TN09AB1234'"""
    return text.replace(" ", "").replace("-", "").upper()    # TODO 1

def is_valid(reg):
    """2 letters, 2 digits, 1-2 letters, 4 digits."""
    if len(reg) not in (9, 10):                               # TODO 2
        return False
    series_len = len(reg) - 8                                 # 1 or 2
    return (reg[:2].isalpha() and reg[2:4].isdigit()
            and reg[4:4 + series_len].isalpha() and reg[-4:].isdigit()
            and reg.isascii())

def format_plate(reg):
    """'TN09AB1234' -> 'TN 09 AB 1234'"""
    if not is_valid(reg):
        raise ValueError("invalid registration: " + reg)
    return " ".join([reg[:2], reg[2:4], reg[4:-4], reg[-4:]])

def is_valid_regex(reg):
    return re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}", reg) is not None

if __name__ == "__main__":
    print("--- Given test ---")
    for raw in ["tn 09 ab 1234", "KA-01-M-0007", "TN9AB1234", "TN 22 1234 AB"]:
        reg = normalise(raw)
        print(f"{raw:15} -> {reg:11} {'valid' if is_valid(reg) else 'INVALID'}")

    print("\n--- Six designed inputs (2 should be rejected) ---")
    tests = [("tn 09 ab 1234", True), ("TN-09-AB-1234", True), ("Tn09Ab1234", True),
             ("ka01m0007", True), ("TN09ABC1234", False), ("T109AB1234", False)]
    for raw, expected in tests:
        reg = normalise(raw); ok = is_valid(reg)
        out = format_plate(reg) if ok else "(rejected)"
        print(f"{raw:16} -> {reg:12} valid={ok!s:5} expected={expected!s:5} receipt={out}")

    print("\n--- Slicing on 9 and 10 character numbers ---")
    for s in ("KA01M0007", "TN09AB1234"):
        print(f"s={s} len={len(s)} s[-4:]={s[-4:]!r} s[4:-4]={s[4:-4]!r}")

    print("\n--- Immutability ---")
    t = "tn09ab1234"; u = t.upper()
    print("text.upper() ->", u, "| text still ->", t)
    try:
        t[0] = "T"
    except TypeError as e:
        print("t[0]='T' ->", type(e).__name__ + ":", e)

    print("\n--- Slicing vs regex: agreement and time ---")
    pool = ["TN09AB1234","KA01M0007","TN9AB1234","TN221234AB","MH12XYZ1234","","AB12C3456","TN09AB12345"]
    print("agree on pool:", all(is_valid(p) == is_valid_regex(p) for p in pool))
    print("lowercase input 'tn09ab1234' (not normalised): slicing =", is_valid("tn09ab1234"),
          "| regex =", is_valid_regex("tn09ab1234"), "-> always normalise first")
    N = 300_000
    for name, fn in [("slicing", is_valid), ("regex", is_valid_regex)]:
        t0 = time.perf_counter()
        for _ in range(N):
            fn("TN09AB1234")
        print(f"{name:<8}: {(time.perf_counter()-t0)/N*1e6:.3f} us per validation")
