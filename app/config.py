"""Configuration. Owned by T01 (frozen afterwards).

Reads environment variables. DATABASE and UPLOAD_DIR default to paths under the
instance folder; the defaults are filled in by create_app() because the instance
path is only known once the Flask app exists.
"""

import os
import secrets
from datetime import timedelta


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    DATABASE = os.environ.get("DATABASE")  # default filled in by create_app()
    UPLOAD_DIR = os.environ.get("UPLOAD_DIR")  # default filled in by create_app()
    MAX_UPLOAD_MB = int(os.environ.get("MAX_UPLOAD_MB", "2"))
    MAX_CONTENT_LENGTH = MAX_UPLOAD_MB * 1024 * 1024
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE") == "1"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
