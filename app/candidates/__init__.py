from flask import Blueprint
bp = Blueprint("candidates", __name__)
from . import routes_profile  # noqa: E402,F401
from . import routes_resume  # noqa: E402,F401
