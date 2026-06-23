# datasheetLoader.py
# Legge un datasheet motore dal formato CSV canonico (long-format), usando
# SOLO la libreria standard. Una riga = un punto di misura; le righe con
# stessi (kv, voltage_V, prop) vengono ricomposte in un unico blocco-vettore.
import csv

# Campi scalari che identificano il blocco (condizione di prova).
_SCALAR_FIELDS = ("kv", "voltage_V", "prop")
# Campi vettoriali: una lista per blocco, un valore per riga del CSV.
_VECTOR_FIELDS = ("throttle_pct", "current_A", "power_W",
                  "thrust_g", "rpm", "efficiency_gW")


def _to_float(value):
    s = str(value).strip().replace("%", "").replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def load_datasheet_csv(path):
    """
    Legge il CSV canonico e restituisce una LISTA di blocchi, IDENTICA per
    struttura a quella del vecchio loader HTML:
      {"kv": "KV780", "voltage_V": 14.8, "prop": "T-MOTOR 9545B",
       "throttle_pct": [...], "current_A": [...], "thrust_g": [...], ...}
    """
    blocchi = {}   # (kv, voltage_V, prop) -> blocco
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        mancanti = (set(_SCALAR_FIELDS) | set(_VECTOR_FIELDS)) - set(reader.fieldnames or [])
        if mancanti:
            raise ValueError(f"Colonne mancanti nel CSV {path}: {sorted(mancanti)}")

        for riga in reader:
            kv = (riga["kv"] or "").strip()
            if not kv:                      # salta righe vuote / commenti
                continue
            voltage = _to_float(riga["voltage_V"])
            prop = (riga["prop"] or "").strip()

            chiave = (kv, voltage, prop)
            if chiave not in blocchi:
                blocco = {"kv": kv, "voltage_V": voltage, "prop": prop}
                for c in _VECTOR_FIELDS:
                    blocco[c] = []
                blocchi[chiave] = blocco

            blocco = blocchi[chiave]
            for c in _VECTOR_FIELDS:
                blocco[c].append(_to_float(riga[c]))

    return list(blocchi.values())


def selectBlock_csv(blocchi, kv=None, voltage=None, prop=None):
    """
    Restituisce l'UNICO blocco che corrisponde ai criteri dati.
    I criteri None vengono ignorati. Errore se nessuno o piu' di uno corrisponde.
    """
    risultati = []
    for b in blocchi:
        if kv is not None and b["kv"] != kv:
            continue
        if voltage is not None and b["voltage_V"] != voltage:
            continue
        if prop is not None and b["prop"] != prop:
            continue
        risultati.append(b)

    if len(risultati) == 0:
        raise ValueError(
            f"Nessun blocco per kv={kv}, voltage={voltage}, prop={prop}")
    if len(risultati) > 1:
        descr = [(b["kv"], b["voltage_V"], b["prop"]) for b in risultati]
        raise ValueError(
            f"Piu' blocchi corrispondono, criteri ambigui: {descr}")
    return risultati[0]