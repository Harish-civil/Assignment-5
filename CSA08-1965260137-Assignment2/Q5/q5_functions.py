"""Q5 - Functions, parameters, scope. Author: M Ayaan (1965260137) | CSA0809"""

def add_item_buggy(item, order=[]):
    order.append(item)
    return order

def add_item(item, order=None):
    if order is None:               # TODO 1
        order = []
    order.append(item)
    return order

# --- Alternative: closure ---
def make_order():
    order = []
    def add(item):
        order.append(item)
        return list(order)
    return add

# --- Parameters ---
def price(item, qty=1, *, gst_rate=0.05, unit=10):
    """positional: item, qty(default 1); keyword-only: gst_rate, unit"""
    return item, qty * unit * (1 + gst_rate)

def bill(prices, gst_rate=0.05):
    """returns TWO values (a tuple): total and GST."""
    subtotal = sum(prices)
    gst = round(subtotal * gst_rate, 2)
    return round(subtotal + gst, 2), gst

# --- Scope ---
counter = 0
def bump_without_global():
    try:
        counter += 1                 # UnboundLocalError
    except UnboundLocalError as e:
        return "UnboundLocalError: " + str(e)

def bump_with_global():
    global counter
    counter += 1
    return counter

def make_counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count
    return inc

def local_shadow():
    counter = 99                     # new local, global untouched
    return counter

if __name__ == "__main__":
    print(add_item_buggy("Tea"), add_item_buggy("Vada"))
    print(add_item("Tea"), add_item("Vada"))
    print("add_item_buggy.__defaults__ =", add_item_buggy.__defaults__)
    print("add_item.__defaults__       =", add_item.__defaults__)

    print("\n3 customers in sequence (fixed design):")
    for name, items in [("Customer A", ["Tea", "Vada"]), ("Customer B", ["Coffee"]), ("Customer C", ["Dosa", "Idli", "Tea"])]:
        o = None
        for it in items:
            o = add_item(it, o)
        print(f"  {name}: {o}")
    print("  default untouched:", add_item.__defaults__)

    print("\n3 customers with the BUGGY function (shared default):")
    for name, items in [("Customer A", ["Tea", "Vada"]), ("Customer B", ["Coffee"]), ("Customer C", ["Dosa"])]:
        o = None
        for it in items:
            o = add_item_buggy(it)
        print(f"  {name}: {o}")
    print("  buggy defaults now:", add_item_buggy.__defaults__)

    print("\nClosure design:")
    a, b = make_order(), make_order()
    a("Tea"); a("Vada"); b("Coffee")
    print("  A:", a("Idli"), "| B:", b("Dosa"))

    print("\nParameters:")
    print("  price('Tea')                       ->", price("Tea"))
    print("  price('Tea', 3)                    ->", price("Tea", 3))
    print("  price(qty=2, item='Vada', unit=12) ->", price(qty=2, item="Vada", unit=12))
    total, gst = bill([30, 12, 20])
    print("  bill([30,12,20]) -> total, gst =", total, gst)

    print("\nScope:")
    print("  without global :", bump_without_global())
    print("  with global    :", bump_with_global(), "| module counter =", counter)
    c = make_counter(); c(); c()
    print("  nonlocal closure counter after 3 calls:", c())
    print("  local shadow   :", local_shadow(), "| global counter still", counter)
