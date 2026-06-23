# datasheetLoader.py
# Legge un datasheet T-Motor (HTML salvato come .xls) usando SOLO la
# libreria standard di Python: nessun pacchetto da installare.
import re
from html.parser import HTMLParser

_COLUMN_MAP = {
    "Throttle":         "throttle_pct",
    "Current (A)":      "current_A",
    "Power (W)":        "power_W",
    "Thrust (G)":       "thrust_g",
    "RPM":              "rpm",
    "Efficiency (G/W)": "efficiency_gW",
}


class _TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self._row = None
        self._cell = None
        self._rowspan = 1

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._row = []
        elif tag == "td" and self._row is not None:
            self._cell = []
            self._rowspan = int(dict(attrs).get("rowspan", 1))

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag):
        if tag == "td" and self._cell is not None:
            testo = " ".join("".join(self._cell).split())
            self._row.append((testo, self._rowspan))
            self._cell = None
        elif tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None


def _fill_rowspans(raw_rows):
    grid = []
    carry = {}
    for raw in raw_rows:
        row = []
        col = 0
        it = iter(raw)
        while True:
            if col in carry:
                row.append(carry[col][0])
                carry[col][1] -= 1
                if carry[col][1] == 0:
                    del carry[col]
                col += 1
                continue
            try:
                testo, rowspan = next(it)
            except StopIteration:
                break
            row.append(testo)
            if rowspan > 1:
                carry[col] = [testo, rowspan - 1]
            col += 1
        grid.append(row)
    return grid


def _to_float(value):
    s = str(value).strip().replace("%", "").replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def load_datasheet(path):
    """
    Legge il datasheet e restituisce una LISTA di blocchi.
    Ogni blocco e' una condizione di prova (kv, tensione, elica) con i suoi vettori:
      {"kv": "KV780", "voltage_V": 14.8, "prop": "T-MOTOR 9545B",
       "throttle_pct": [...], "current_A": [...], "thrust_g": [...], ...}
    """
    with open(path, encoding="utf-8") as f:
        parser = _TableParser()
        parser.feed(f.read())

    grid = _fill_rowspans(parser.rows)
    idx = {nome: i for i, nome in enumerate(grid[0])}

    blocchi = {}   # (kv, tensione, prop) -> blocco
    for row in grid[1:]:
        if not row or row[0].startswith("Notes:"):
            continue
        match = re.search(r"KV\d+", row[0])
        if not match:
            continue
        kv = match.group(0)
        tensione = _to_float(row[idx["Voltage (V)"]]) if "Voltage (V)" in idx else None
        prop = row[idx["Prop"]] if "Prop" in idx else None

        chiave = (kv, tensione, prop)
        if chiave not in blocchi:
            blocco = {"kv": kv, "voltage_V": tensione, "prop": prop}
            for c in _COLUMN_MAP.values():
                blocco[c] = []
            blocchi[chiave] = blocco

        blocco = blocchi[chiave]
        for col_datasheet, c in _COLUMN_MAP.items():
            if col_datasheet in idx:
                blocco[c].append(_to_float(row[idx[col_datasheet]]))

    return list(blocchi.values())


def selectBlock(blocchi, kv=None, voltage=None, prop=None):
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
