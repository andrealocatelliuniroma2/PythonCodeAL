# Author: Andrea Locatelli <andrea.locatelli.1997@gmail.com>
# Copyright (c) 2026 Andrea Locatelli

# displayDatasheet.py
def displayDatasheet(blocks):
    """Prints each datasheet block as a readable table."""
    columns = [
        ("throttle_pct",  "Throttle(%)"),
        ("current_A",     "Current(A)"),
        ("power_W",       "Power(W)"),
        ("thrust_g",      "Thrust(g)"),
        ("rpm",           "RPM"),
        ("efficiency_gW", "Eff(g/W)"),
    ]
    width = 12

    for b in blocks:
        print(f"\n=== {b['kv']} @ {b['voltage_V']} V — Prop: {b['prop']} ===")
        header = "".join(f"{name:>{width}}" for _, name in columns)
        print(header)
        print("-" * len(header))
        for i in range(len(b["throttle_pct"])):
            row = "".join(f"{b[key][i]:>{width}}" for key, _ in columns)
            print(row)