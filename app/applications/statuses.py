"""Application statuses from FP-EMP-3."""

STATUSES: tuple[str, ...] = ("pending", "interviewing", "rejected", "accepted")
LABELS: dict[str, str] = {
    "pending": "Pending",
    "interviewing": "Interviewing",
    "rejected": "Rejected",
    "accepted": "Accepted",
}
TRANSITIONS: dict[str, tuple[str, ...]] = {
    status: tuple(other for other in STATUSES if other != status)
    for status in STATUSES
}
