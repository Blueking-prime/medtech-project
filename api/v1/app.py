#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views, AUTH
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from typing import Tuple


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
host = getenv("API_HOST", "0.0.0.0")
port = getenv("API_PORT", "5000")

@app.before_first_request
def authorize():
    '''Authenticates the user'''
    pass


@app.errorhandler(404)
def not_found(error) -> Tuple:
    """ Not found handler
    """
    return jsonify({"error": f"Not found. Visit http://{host}:{port}/api/v1/info' for help"}), 404


@app.errorhandler(401)
def unauthorized(error) -> Tuple:
    ''' Unauthorized handler'''
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> Tuple:
    ''' Forbidden handler'''
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)
