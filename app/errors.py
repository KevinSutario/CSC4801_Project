"""Error classes and HTTP error handlers. Owned by T01 (frozen afterwards).

Routes catch ValidationError themselves and re-render the form with status 400.
"""

from flask import Flask, render_template
from werkzeug.exceptions import HTTPException


class ServiceError(Exception):
    """Base class for errors raised by services."""


class ValidationError(ServiceError):
    def __init__(self, errors: dict[str, str]) -> None:
        self.errors = errors
        super().__init__(str(errors))


class NotFound(ServiceError):
    pass


class Forbidden(ServiceError):
    pass


class Conflict(ServiceError):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


def init_app(app: Flask) -> None:
    @app.errorhandler(NotFound)
    def handle_not_found(e: NotFound):
        return render_template("errors/404.html"), 404

    @app.errorhandler(Forbidden)
    def handle_forbidden(e: Forbidden):
        return render_template("errors/403.html"), 403

    @app.errorhandler(Conflict)
    def handle_conflict(e: Conflict):
        return render_template("errors/409.html", message=e.message), 409

    @app.errorhandler(400)
    def handle_400(e: HTTPException):
        return render_template("errors/400.html"), 400

    @app.errorhandler(403)
    def handle_403(e: HTTPException):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def handle_404(e: HTTPException):
        return render_template("errors/404.html"), 404

    @app.errorhandler(405)
    def handle_405(e: HTTPException):
        return render_template("errors/405.html"), 405

    @app.errorhandler(413)
    def handle_413(e: HTTPException):
        return render_template("errors/413.html"), 413

    @app.errorhandler(500)
    def handle_500(e: HTTPException):
        return render_template("errors/500.html"), 500
