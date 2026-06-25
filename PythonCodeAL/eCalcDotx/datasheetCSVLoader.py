# datasheetLoader.py
# Reads a motor datasheet from the canonical CSV format (long-format), using
# ONLY the standard library. One row = one measurement point; rows with
# the same (kv, voltage_V, prop) are recombined into a single vector-block.
import csv

# Scalar fields identifying the block (test condition).
_SCALAR_FIELDS = ("kv", "voltage_V", "prop")
# Vector fields: one list per block, one value per CSV row.
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
    Reads the canonical CSV and returns a LIST of blocks, IDENTICAL in
    structure to the one from the old HTML loader:
    {"kv": "KV780", "voltage_V": 14.8, "prop": "T-MOTOR 9545B",
    "throttle_pct": [...], "current_A": [...], "thrust_g": [...], ...}
    """
    blocks = {}   # (kv, voltage_V, prop) -> block
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        missing = (set(_SCALAR_FIELDS) | set(_VECTOR_FIELDS)) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing columns in CSV {path}: {sorted(missing)}")

        for row in reader:
            kv = (row["kv"] or "").strip()
            if not kv:                      # skip empty rows / comments
                continue
            voltage = _to_float(row["voltage_V"])
            prop = (row["prop"] or "").strip()

            key = (kv, voltage, prop)
            if key not in blocks:
                block = {"kv": kv, "voltage_V": voltage, "prop": prop}
                for c in _VECTOR_FIELDS:
                    block[c] = []
                blocks[key] = block

            block = blocks[key]
            for c in _VECTOR_FIELDS:
                block[c].append(_to_float(row[c]))

    return list(blocks.values())


def selectBlock_csv(blocks, kv=None, voltage=None, prop=None):
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