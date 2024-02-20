#!/usr/bin/env python3
"""FLask App module
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def get_index():
    """Basic Flask app
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
