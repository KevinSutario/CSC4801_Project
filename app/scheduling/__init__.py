from flask import Blueprint
bp = Blueprint("scheduling", __name__)
from . import routes_employer  # noqa: E402,F401
from . import routes_candidate  # noqa: E402,F401
