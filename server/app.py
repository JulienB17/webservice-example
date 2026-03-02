#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask API layer for segmented linear regression.

Responsibilities:
- Receive JSON request
- Validate input
- Call scientific functions
- Return JSON response

@author: julienbarneoud
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

#internal import
import toolbox as tb

# ----------------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------------
HOST = "127.0.0.1"
PORT = 5000
DEBUG = True

# ----------------------------------------------------------------------
# FLASK APPLICATION
# ----------------------------------------------------------------------

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=["GET"])
def super_endpoint():
    
    return "Welcome to the webservice API !"


@app.route("/api/linear_trend", methods=["POST"])
def linear_trend():
    """
    Expected JSON input:
    --------------------
    {
        "x": [...],
        "y": [...],
        "disc": [...]
    }

    JSON response:
    --------------
    {
        "series": [{x:[], y:[], a:float, b:float}, ...],
        "image": "base64_string"
    }
    """

    data = request.json

    x = data.get("x", [])
    y = data.get("y", [])
    disc = data.get("disc", [])
    x_label = data.get("x_label", "x")
    y_label = data.get("y_label", "y")

    if len(x) != len(y):
        return jsonify({"error": "x and y must have same length"}), 400

    series = tb.compute_trends(x, y, disc)

    image = tb.generate_plot(series, disc, x_label, y_label)

    return jsonify({
        "series": series,
        "disc": disc,              # returned disc list (client plot...)
        "x_label": x_label,
        "y_label": y_label,
        "image": image
    })


if __name__ == "__main__":
    # Debug mode for development only
    print("Starting Flask server...")
    print(f"Host  : {HOST}")
    print(f"Port  : {PORT}")
    print(f"Debug : {DEBUG}")

    app.run(host=HOST, port=PORT, debug=DEBUG)
