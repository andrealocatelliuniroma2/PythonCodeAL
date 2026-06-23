# displayDatasheet.py
def displayDatasheet(blocchi):
    """Stampa ogni blocco del datasheet come tabella leggibile."""
    colonne = [
        ("throttle_pct",  "Throttle(%)"),
        ("current_A",     "Current(A)"),
        ("power_W",       "Power(W)"),
        ("thrust_g",      "Thrust(g)"),
        ("rpm",           "RPM"),
        ("efficiency_gW", "Eff(g/W)"),
    ]
    larghezza = 12

    for b in blocchi:
        print(f"\n=== {b['kv']} @ {b['voltage_V']} V — Prop: {b['prop']} ===")
        intestazione = "".join(f"{nome:>{larghezza}}" for _, nome in colonne)
        print(intestazione)
        print("-" * len(intestazione))
        for i in range(len(b["throttle_pct"])):
            riga = "".join(f"{b[chiave][i]:>{larghezza}}" for chiave, _ in colonne)
            print(riga)
