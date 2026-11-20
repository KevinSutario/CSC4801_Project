"""Timezone utility tests. Owned by T12 (no template test names; T12 adds its own
tests here).

FP-SCHED-1 requires "an unambiguous, documented timezone" and correct display in
any zone; these tests cover the Hong Kong -> UTC -> London conversion chain, the
New York DST gap, the fixed-seed round trip and unknown-zone rejection.
"""

import random
from datetime import datetime, timedelta

import pytest

from app import timeutil

# 2030-01-07 10:00 Asia/Hong_Kong == 2030-01-07T02:00:00Z (UTC+8, no DST).
# In January London is on GMT (UTC+0), so the same instant shows as 02:00.
_HK_DATE, _HK_TIME = "2030-01-07", "10:00"


def test_hk_local_to_utc():
    assert timeutil.local_to_utc(_HK_DATE, _HK_TIME, "Asia/Hong_Kong") == "2030-01-07T02:00:00Z"


def test_shown_in_london():
    shown = timeutil.utc_to_local("2030-01-07T02:00:00Z", "Europe/London")
    assert shown.replace(tzinfo=None) == datetime(2030, 1, 7, 2, 0)


def test_nyc_dst_gap_raises():
    # 02:30 local does not exist on 2030-03-10 (clocks jump 02:00 -> 03:00).
    with pytest.raises(ValueError):
        timeutil.local_to_utc("2030-03-10", "02:30", "America/New_York")


def test_round_trip_random_local_times():
    rng = random.Random(20261120)
    zones = ["Asia/Hong_Kong", "Europe/London", "America/New_York"]
    checked = 0
    for _ in range(200):
        zone = rng.choice(zones)
        local = datetime(2030, 1, 1) + timedelta(minutes=rng.randrange(60 * 24 * 365))
        date_str = local.strftime("%Y-%m-%d")
        time_str = local.strftime("%H:%M")
        try:
            utc_iso = timeutil.local_to_utc(date_str, time_str, zone)
        except ValueError:
            continue  # a nonexistent local time (DST gap); not a round-trip case
        back = timeutil.utc_to_local(utc_iso, zone)
        assert back.strftime("%Y-%m-%d %H:%M") == f"{date_str} {time_str}"
        checked += 1
    assert checked >= 190  # the gap days are rare; almost all draws must round-trip


def test_validate_tz_unknown_zone_raises():
    with pytest.raises(ValueError):
        timeutil.validate_tz("Mars/Base")


def test_validate_tz_common_zones_ok():
    for zone in timeutil.COMMON_TIMEZONES:
        assert timeutil.validate_tz(zone) == zone
