"""Candidate scheduling routes (FP-SCHED-2). Owned by T16, then T17.

/candidate/applications/<id> shows the application with either the open slots
(the candidate's zone) or the booked slot; /book/<slot_id> is the confirm
screen (GET) and the booking POST. All candidate-only; every POST form carries
csrf_field(). Booking refusals re-render book.html with the message
(DEFAULT, not in brief).
"""

from flask import flash, g, redirect, render_template

from app import timeutil
from app.applications.service import get_own_application
from app.applications.statuses import LABELS
from app.candidates.profile_service import get_profile
from app.db import get_db
from app.errors import Conflict, Forbidden, NotFound
from app.security import role_required

from . import bp
from . import booking as booking_service

_BADGE_TONES = {
    "pending": "pending",
    "interviewing": "info",
    "rejected": "danger",
    "accepted": "success",
}


def _candidate_zone(conn, candidate_id: int) -> str:
    """The candidate's profile zone, or UTC if it is somehow invalid."""
    timezone = get_profile(conn, candidate_id)["timezone"]
    try:
        return timeutil.validate_tz(timezone)
    except ValueError:
        return "UTC"


def _view_model(conn, application_id: int) -> dict:
    """The data the detail page needs: application, zone, bookable slots."""
    candidate_id = g.user["id"]
    application = get_own_application(conn, candidate_id, application_id)
    zone = _candidate_zone(conn, candidate_id)
    slots = booking_service.list_bookable_slots(conn, candidate_id, application_id)
    return {
        "application": application,
        "zone": zone,
        "slots": slots,
        "eligible": booking_service.is_eligible(conn, candidate_id, application_id),
        "labels": LABELS,
        "badge_tones": _BADGE_TONES,
        "utc_to_local": timeutil.utc_to_local,
    }


@bp.get("/candidate/applications/<int:application_id>")
@role_required("candidate")
def application_detail(application_id: int):
    conn = get_db()
    return render_template("scheduling/book.html", **_view_model(conn, application_id))


@bp.get("/candidate/applications/<int:application_id>/book/<int:slot_id>")
@role_required("candidate")
def confirm_booking(application_id: int, slot_id: int):
    conn = get_db()
    candidate_id = g.user["id"]
    # Ownership first (NotFound / Forbidden from get_own_application), then the
    # slot must be one of this application's currently bookable slots.
    get_own_application(conn, candidate_id, application_id)
    slots = booking_service.list_bookable_slots(conn, candidate_id, application_id)
    slot = next((s for s in slots if s["id"] == slot_id), None)
    if slot is None:
        raise NotFound()
    application = get_own_application(conn, candidate_id, application_id)
    zone = _candidate_zone(conn, candidate_id)
    return render_template(
        "scheduling/confirm_booking.html", application=application, slot=slot,
        zone=zone, utc_to_local=timeutil.utc_to_local,
    )


@bp.post("/candidate/applications/<int:application_id>/book/<int:slot_id>")
@role_required("candidate")
def book(application_id: int, slot_id: int):
    conn = get_db()
    candidate_id = g.user["id"]
    try:
        booking_service.book_slot(conn, candidate_id, application_id, slot_id)
    except Conflict as exc:
        model = _view_model(conn, application_id)
        return render_template("scheduling/book.html", message=exc.message, **model), 409
    except Forbidden:
        model = _view_model(conn, application_id)
        return render_template(
            "scheduling/book.html",
            message="Booking is not available for this application.", **model
        ), 403
    flash("Interview booked", "success")
    return redirect(f"/candidate/applications/{application_id}")
