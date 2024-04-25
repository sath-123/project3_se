# application/user_api/__init__.py
from flask import Blueprint

vendor_api_blueprint = Blueprint('vendor_api', __name__)

from . import routes
