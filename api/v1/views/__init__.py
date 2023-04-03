#!/usr/bin/env python3
'''Views module initializer'''
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.medication import *

User.load_from_file()

from api.v1.views.auth import *
