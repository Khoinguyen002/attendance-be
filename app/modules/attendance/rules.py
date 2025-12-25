from datetime import datetime, time
import os
import pytz

from app.config import Config


TZ = pytz.timezone(Config.TIMEZONE)


def _parse_time(value: str) -> time:
    h, m = value.split(":")
    return time(int(h), int(m))


WORK_START = _parse_time(Config.WORK_START)
WORK_END = _parse_time(Config.WORK_END)


def evaluate_attendance(daily: dict) -> dict:
    """
    Input: attendance_daily record
    Output: {
        status: full | late | early | late_early | absent,
        late_minutes: int,
        early_minutes: int
    }
    """

    if not daily.get("check_in"):
        return {
            "status": "absent",
            "late_minutes": 0,
            "early_minutes": 0
        }

    check_in = daily["check_in"].astimezone(TZ)
    check_out = daily.get("check_out")

    start_dt = datetime.combine(
        check_in.date(), WORK_START, TZ
    )

    end_dt = datetime.combine(
        check_in.date(), WORK_END, TZ
    )

    late_minutes = max(
        int((check_in - start_dt).total_seconds() / 60), 0
    )

    early_minutes = 0
    if check_out:
        check_out = check_out.astimezone(TZ)
        early_minutes = max(
            int((end_dt - check_out).total_seconds() / 60), 0
        )

    # status
    if late_minutes > 0 and early_minutes > 0:
        status = "late_early"
    elif late_minutes > 0:
        status = "late"
    elif early_minutes > 0:
        status = "early"
    else:
        status = "full"

    return {
        "status": status,
        "late_minutes": late_minutes,
        "early_minutes": early_minutes
    }
