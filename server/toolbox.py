#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Scientific computation module for the web service.

Responsibilities:
- Split the dataset into segments based on discontinuities
- Compute linear regression for each segment
- Generate a PNG plot encoded in base64
- ...

@author: julienbarneoud
"""

import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from typing import List, Tuple, Dict


# ----------------------------------------------------------------------
# DATA SEGMENTATION
# ----------------------------------------------------------------------

def segment_data(x,  y, disc):
    """
    Split the time series into segments according to discontinuities.

    Parameters
    ----------
    x : np.ndarray
        Array of x values (must be sorted).
    y : np.ndarray
        Array of y values.
    disc : list of float
        List of x-values where a discontinuity occurs.

    Returns
    -------
    segments : list of (x_segment, y_segment)
        Each segment is a tuple of numpy arrays.

    Teaching note
    -------------
    We use numpy.searchsorted to efficiently find
    the index corresponding to each discontinuity.
    """

    # Ensure discontinuities are sorted
    disc_sorted = sorted(disc)

    segments = []
    current_start = 0

    for d in disc_sorted:
        # Find index where d should be inserted
        idx = np.searchsorted(x, d)

        segments.append((x[current_start:idx],
                         y[current_start:idx]))

        current_start = idx

    # Add final segment
    segments.append((x[current_start:], y[current_start:]))

    return segments


# ----------------------------------------------------------------------
# LINEAR TREND COMPUTATION
# ----------------------------------------------------------------------

def compute_trends(x, y, disc):
    """
    Compute linear regression y = a*x + b
    for each segment defined by discontinuities.

    Parameters
    ----------
    x : list of float
        X values received from client (JSON).
    y : list of float
        Y values received from client (JSON).
    disc : list of float
        Discontinuities provided by the user.

    Returns
    -------
    results : list of dict
        One dictionary per segment containing:
            - x : segment x values
            - y : segment y values
            - a : slope
            - b : intercept

    Method
    ------
    We use numpy.polyfit with degree 1.
    """

    # Convert Python lists into numpy arrays
    x = np.array(x)
    y = np.array(y)

    segments = segment_data(x, y, disc)

    results = []

    for xs, ys in segments:

        # At least 2 points are required for regression
        if len(xs) < 2:
            continue

        # Linear regression (degree 1 polynomial fit)
        a, b = np.polyfit(xs, ys, 1)

        results.append({
            "x": xs.tolist(),
            "y": ys.tolist(),
            "a": float(a),
            "b": float(b)
        })

    return results


# ----------------------------------------------------------------------
# PLOT GENERATION
# ----------------------------------------------------------------------

def generate_plot(series, disc, x_label="x", y_label="y"):
    """
    Generate PNG plot encoded in base64.

    Features:
    - Black scatter for data
    - Red lines for linear models
    - Blue vertical lines for discontinuities
    """

    plt.figure()

    first_segment = True

    for seg in series:
        xs = np.array(seg["x"])
        ys = np.array(seg["y"])
        a = seg["a"]
        b = seg["b"]

        # Plot data (black scatter)
        if first_segment:
            plt.plot(xs, ys, '.', color="black", label="data")
        else:
            plt.plot(xs, ys, '.', color="black")

        # Plot model (red line)
        if first_segment:
            plt.plot(xs, a * xs + b, color="red", label="model", linewidth=2)
        else:
            plt.plot(xs, a * xs + b, color="red",  linewidth=2)

        first_segment = False

    # Plot discontinuities
    for i, d in enumerate(disc):
        if i == 0:
            plt.axvline(x=d, color="blue", linestyle="--", label="disc")
        else:
            plt.axvline(x=d, color="blue", linestyle="--")

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title("Segmented Linear Trends")
    plt.tight_layout()
    plt.legend()
    plt.grid()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()

    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    return image_base64