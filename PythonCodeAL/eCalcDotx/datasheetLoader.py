# Author: Andrea Locatelli <andrea.locatelli.1997@gmail.com>
# Copyright (c) 2026 Andrea Locatelli

# datasheetLoader.py
# Reads a T-Motor datasheet (HTML saved as .xls) using ONLY the
# Python standard library: no packages to install.
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
            text = " ".join("".join(self._cell).split())
            self._row.append((text, self._rowspan))
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
                text, rowspan = next(it)
            except StopIteration:
                break
            row.append(text)
            if rowspan > 1:
                carry[col] = [text, rowspan - 1]
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
    Reads the datasheet and returns a LIST of blocks.
    Each block is a test condition (kv, voltage, propeller) with its vectors:
      {"kv": "KV780", "voltage_V": 14.8, "prop": "T-MOTOR 9545B",
       "throttle_pct": [...], "current_A": [...], "thrust_g": [...], ...}
    """
    with open(path, encoding="utf-8") as f:
        parser = _TableParser()
        parser.feed(f.read())

    grid = _fill_rowspans(parser.rows)
    idx = {name: i for i, name in enumerate(grid[0])}

    blocks = {}   # (kv, voltage, prop) -> block
    for row in grid[1:]:
        if not row or row[0].startswith("Notes:"):
            continue
        match = re.search(r"KV\d+", row[0])
        if not match:
            continue
        kv = match.group(0)
        voltage = _to_float(row[idx["Voltage (V)"]]) if "Voltage (V)" in idx else None
        prop = row[idx["Prop"]] if "Prop" in idx else None

        key = (kv, voltage, prop)
        if key not in blocks:
            block = {"kv": kv, "voltage_V": voltage, "prop": prop}
            for c in _COLUMN_MAP.values():
                block[c] = []
            blocks[key] = block

        block = blocks[key]
        for col_datasheet, c in _COLUMN_MAP.items():
            if col_datasheet in idx:
                block[c].append(_to_float(row[idx[col_datasheet]]))

    return list(blocks.values())


def selectBlock(blocks, kv=None, voltage=None, prop=None):
    """
    Returns the SINGLE block matching the given criteria.
    None criteria are ignored. Raises an error if none or more than one matches.
    """
    results = []
    for b in blocks:
        if kv is not None and b["kv"] != kv:
            continue
        if voltage is not None and b["voltage_V"] != voltage:
            continue
        if prop is not None and b["prop"] != prop:
            continue
        results.append(b)

    if len(results) == 0:
        raise ValueError(
            f"No block found for kv={kv}, voltage={voltage}, prop={prop}")
    if len(results) > 1:
        descr = [(b["kv"], b["voltage_V"], b["prop"]) for b in results]
        raise ValueError(
            f"Multiple blocks match, ambiguous criteria: {descr}")
    return results[0]