# currentEstimate.py
# Interpolazione lineare con la sola libreria standard (niente numpy).
from bisect import bisect_left

def estimateCurrent(thrust_query, thrust_data, current_data,
                    allow_extrapolation=False):
    """
    Stima la corrente (A) a una data spinta (g) per interpolazione lineare.
    thrust_query : spinta richiesta per singolo motore [g]
    thrust_data  : vettore delle spinte dal datasheet (le x)
    current_data : vettore delle correnti dal datasheet (le y)
    """
    punti = sorted(zip(thrust_data, current_data))
    xs = [p[0] for p in punti]
    ys = [p[1] for p in punti]

    if not allow_extrapolation and (thrust_query < xs[0] or thrust_query > xs[-1]):
        raise ValueError(
            f"spinta {thrust_query} g fuori dal range datasheet "
            f"[{xs[0]}, {xs[-1]}] g: estrapolazione non consentita")

    if thrust_query <= xs[0]:
        return ys[0]
    if thrust_query >= xs[-1]:
        return ys[-1]

    i = bisect_left(xs, thrust_query)
    x0, x1 = xs[i - 1], xs[i]
    y0, y1 = ys[i - 1], ys[i]

    return y0 + (thrust_query - x0) / (x1 - x0) * (y1 - y0)