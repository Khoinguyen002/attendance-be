from datetime import datetime
from bson import ObjectId

from app.extensions.mongo import mongo
from app.modules.attendance.utils import today_str


def scan_attendance(employee_id: str):
    employee_oid = ObjectId(employee_id)
    today = today_str()
    now = datetime.utcnow()

    daily = mongo.db.attendance_daily.find_one({
        "employee_id": employee_oid,
        "date": today
    })

    if not daily:
        mongo.db.attendance_logs.insert_one({
            "employee_id": employee_oid,
            "type": "check_in",
            "timestamp": now
        })

        mongo.db.attendance_daily.insert_one({
            "employee_id": employee_oid,
            "date": today,
            "check_in": now,
            "check_out": None,
            "worked_minutes": 0
        })

        return "check_in"

    # ⛔ ĐÃ CHECK-OUT
    if daily.get("check_out"):
        raise ValueError("Already checked out today")

    # ⏱ CHECK-OUT
    worked_minutes = int(
        (now - daily["check_in"]).total_seconds() / 60
    )

    mongo.db.attendance_logs.insert_one({
        "employee_id": employee_oid,
        "type": "check_out",
        "timestamp": now
    })

    mongo.db.attendance_daily.update_one(
        {"_id": daily["_id"]},
        {
            "$set": {
                "check_out": now,
                "worked_minutes": worked_minutes
            }
        }
    )

    return "check_out"
