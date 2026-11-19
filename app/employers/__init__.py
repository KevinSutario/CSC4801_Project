from flask import Blueprint
bp = Blueprint("employers", __name__)
from . import routes  # noqa: E402,F401
