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

from flask import Flask, request, jsonify, Blueprint
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

# NOTE BASE URL (like '/api') configurable; avoids manual '/api/' in routes; can be adjusted at deployment

@app.route('/', methods=["GET"])
def welcome_endpoint():
    
    return "Welcome to the webservice API !"


###############################################################################
#### Webservice main endpoints (trend computation, etc.)
################################################################################

@app.route("/linear_trend", methods=["POST"]) 
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


####################################################################################
###### Tests & examples (GET, POST,...)
##################################################################################

@app.route("/station/<string:country>/<string:name_station>", methods=["GET"])
def get_station(country, name_station):
    """
    Basic GET example using a path parameter.

    URL example:
    http://127.0.0.1:5000/station/USA/GOLD

    The station country & name are part of the URL path.
    This is typically used to identify a specific resource.
    """

    return jsonify({
        "type": "path_parameter",
        "country": country,
        "station": name_station,
        "message": f"Station '{name_station}' in country '{country}' successfully received."
    })


@app.route("/sum", methods=["GET"])
def sum_operation():
    """
    Basic GET example using query parameters.

    URL example:
    http://127.0.0.1:5000/sum?a=10&b=5

    Query parameters are typically used for filters or optional arguments.
    """

    a = request.args.get("a", type=float)
    b = request.args.get("b", type=float)

    if a is None or b is None:
        return jsonify({
            "error": "Missing parameters. Please provide 'a' and 'b'."
        }), 400

    result = a + b

    return jsonify({
        "type": "query_parameter",
        "operation": "addition",
        "a": a,
        "b": b,
        "result": result
    })



if __name__ == "__main__":
    # Debug mode for development only
    print("Starting Flask server...")
    print(f"Host  : {HOST}")
    print(f"Port  : {PORT}")
    print(f"Debug : {DEBUG}")

    app.run(host=HOST, port=PORT, debug=DEBUG)
