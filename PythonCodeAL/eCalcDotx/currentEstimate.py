# Author: Andrea Locatelli <andrea.locatelli.1997@gmail.com>
# Copyright (c) 2026 Andrea Locatelli

# currentEstimate.py

from bisect import bisect_left

def estimateCurrent(thrust_query, thrust_data, current_data,
                    allow_extrapolation=False):
    """
    Estimates the current (A) at a given thrust (g) via linear interpolation.

    Parameters:
    thrust_query : Required thrust per single motor [g]
    thrust_data  : Array of thrust values from datasheet (the x-axis)
    current_data : Array of current values from datasheet (the y-axis)
    """
    points = sorted(zip(thrust_data, current_data))
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    if not allow_extrapolation and (thrust_query < xs[0] or thrust_query > xs[-1]):
        raise ValueError(
            f"Thrust {thrust_query} g out of datasheet range "
            f"[{xs[0]}, {xs[-1]}] g: error interpolation")

    if thrust_query <= xs[0]:
        return ys[0]
    if thrust_query >= xs[-1]:
        return ys[-1]

    i = bisect_left(xs, thrust_query)
    x0, x1 = xs[i - 1], xs[i]
    y0, y1 = ys[i - 1], ys[i]

    return y0 + (thrust_query - x0) / (x1 - x0) * (y1 - y0)