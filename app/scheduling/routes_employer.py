"""Employer scheduling routes. Owned by T12.

/employer/slots shows the add-slot form and the employer's slot list; POST
creates a slot. /employer/slots/<id>/delete deletes an unbooked slot. Both are
employer-only; every POST form carries csrf_field().
"""

from flask import abort, flash, g, redirect, render_template, request

from app import timeutil
from app.db import get_db
from app.errors import Conflict, Forbidden, NotFound, ValidationError
from app.security import role_required

from . import bp
from . import slots as slots_service


def zone_options() -> list[tuple[str, str]]:
    """(value, label) pairs for the time zone select (components/forms.html)."""
    return [(zone, zone) for zone in timeutil.COMMON_TIMEZONES]


def _last_used_zone(conn) -> str:
    """The employer's most recently created slot's zone, or UTC."""
    row = conn.execute(
        "SELECT created_tz FROM interview_slots WHERE employer_id = ?"
        " ORDER BY id DESC LIMIT 1",
        (g.user["id"],),
    ).fetchone()
    if row is None:
        return "UTC"
    try:
        return timeutil.validate_tz(row["created_tz"])
    except ValueError:
        return "UTC"


@bp.route("/employer/slots", methods=["GET", "POST"])
@role_required("employer")
def slots():
    conn = get_db()
    if request.method == "POST":
        values = {
            "date": request.form.get("date", ""),
            "start": request.form.get("start", ""),
            "end": request.form.get("end", ""),
            "timezone": request.form.get("timezone", ""),
        }
        try:
            slots_service.create_slot(conn, g.user["id"], values["date"], values["start"],
                                      values["end"], values["timezone"])
        except ValidationError as exc:
            listed = slots_service.list_slots_for_employer(conn, g.user["id"])
            return render_template("scheduling/slots.html", errors=exc.errors,
                                   form=values, slot_list=listed,
                                   zones=zone_options(),
                                   display_zone=values["timezone"] or "UTC",
                                   utc_to_local=timeutil.utc_to_local), 400
        flash("Slot added", "success")
        return redirect("/employer/slots")
    listed = slots_service.list_slots_for_employer(conn, g.user["id"])
    zone = _last_used_zone(conn)
    return render_template("scheduling/slots.html", errors={},
                           form={"date": "", "start": "", "end": "", "timezone": zone},
                           slot_list=listed, zones=zone_options(),
                           display_zone=zone, utc_to_local=timeutil.utc_to_local)


@bp.post("/employer/slots/<int:slot_id>/delete")
@role_required("employer")
def delete_slot(slot_id: int):
    conn = get_db()
    try:
        slots_service.delete_slot(conn, g.user["id"], slot_id)
    except NotFound:
        abort(404)
    except Forbidden:
        abort(403)
    except Conflict as exc:
        raise exc  # handled by the 409 error handler
    flash("Slot deleted", "success")
    return redirect("/employer/slots")
