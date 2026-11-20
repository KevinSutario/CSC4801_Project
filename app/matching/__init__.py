from flask import Blueprint
bp = Blueprint("matching", __name__)
from . import routes  # noqa: E402,F401
