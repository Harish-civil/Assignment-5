"""Q2 - OTP attempts with while / for / loop-else / recursion.
Author: M Ayaan (1965260137) | CSA0809"""
import sys
CORRECT = "482913"

def verify_while(inputs):
    """while version. Blank entries do not count as attempts (continue)."""
    it = iter(inputs)
    attempts = 0
    while attempts < 3:
        entry = next(it, None)
        if entry is None:
            return "NO MORE INPUT", attempts
        if entry.strip() == "":
            continue                      # blank: do NOT count
        if entry.strip() == CORRECT:
            break                         # success
        attempts += 1                     # counted only for a real wrong try
    else:
        return "LOCKED 30 MIN", attempts  # loop finished without break
    return "SUCCESS", attempts + 1

def verify_for(inputs):
    """for/range(3) version. A blank must be re-asked WITHOUT consuming a range value,
    so an inner while collects a non-blank entry first."""
    it = iter(inputs)
    for attempt in range(3):
        entry = ""
        while entry == "":
            entry = next(it, None)
            if entry is None:
                return "NO MORE INPUT", attempt
            entry = entry.strip()
            if entry == "":
                pass                      # pass: no-op placeholder, loop simply asks again
        if entry == CORRECT:
            break
    else:
        return "LOCKED 30 MIN", 3
    return "SUCCESS", attempt + 1

def verify_while_extra(inputs, security_answer, security_ok="chennai"):
    """Changed condition: 2 extra attempts after a correct security answer.
    The limit is a variable, so only one number changes."""
    it = iter(inputs)
    limit, attempts, extra_given = 3, 0, False
    while True:
        while attempts < limit:
            entry = next(it, None)
            if entry is None:
                return "NO MORE INPUT", attempts
            if entry.strip() == "":
                continue
            if entry.strip() == CORRECT:
                return "SUCCESS", attempts + 1
            attempts += 1
        if not extra_given and security_answer.lower() == security_ok:
            limit += 2
            extra_given = True
            continue
        return "LOCKED 30 MIN", attempts

def verify_recursive(inputs, idx=0, attempts=0):
    """Recursive: each call handles one entry. Stack depth O(a)."""
    if attempts == 3:
        return "LOCKED 30 MIN", attempts
    if idx >= len(inputs):
        return "NO MORE INPUT", attempts
    e = inputs[idx].strip()
    if e == "":
        return verify_recursive(inputs, idx + 1, attempts)
    if e == CORRECT:
        return "SUCCESS", attempts + 1
    return verify_recursive(inputs, idx + 1, attempts + 1)

def buggy_counter(inputs):
    """BUG DEMO: counter incremented at the top of the loop, so blanks are counted."""
    it = iter(inputs); attempts = 0
    while attempts < 3:
        attempts += 1                     # wrong place
        entry = next(it, "")
        if entry.strip() == CORRECT:
            return "SUCCESS", attempts
    return "LOCKED 30 MIN", attempts

SCENARIOS = {
    "correct first try":            ["482913"],
    "wrong, wrong, correct":        ["111111", "222222", "482913"],
    "three wrong":                  ["111111", "222222", "333333"],
    "blank, wrong, blank, correct": ["", "111111", "  ", "482913"],
    "blank x3 then correct":        ["", "", "", "482913"],
    "wrong, blank, wrong, wrong":   ["111111", "", "222222", "333333"],
}

if __name__ == "__main__":
    print(f"{'scenario':<30} {'while':<24} {'for':<24} {'recursive':<24} buggy-counter")
    for name, inp in SCENARIOS.items():
        print(f"{name:<30} {str(verify_while(inp)):<24} {str(verify_for(inp)):<24} "
              f"{str(verify_recursive(inp)):<24} {buggy_counter(inp)}")
    print("\nChanged condition (security answer 'Chennai' -> +2 attempts):")
    t = ["1", "2", "3", "4", "482913"]
    print("  correct OTP on 5th try, security ok  :", verify_while_extra(t, "Chennai"))
    print("  correct OTP on 5th try, security bad :", verify_while_extra(t, "Madurai"))
    print("  6 wrong tries, security ok           :", verify_while_extra(["1","2","3","4","5","6"], "Chennai"))
    print("\nRecursion limit:", sys.getrecursionlimit())
