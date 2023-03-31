#!/usr/bin/env python3
'''Module of basic api routes'''
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})

@app_views.route('/info', methods=['GET'], strict_slashes=False)
def info() -> str:
    """ GET /api/v1/info
    Return:
      - Help about the API
    """
    return jsonify('coming soon')
