from bson import ObjectId
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, get_jwt
from app.common.decorators import role_required
from app.extensions.mongo import mongo, to_object_id
from app.modules.attendance.qr import decode_qr_payload, generate_qr_token, verify_qr_token
from app.modules.attendance.service import scan_attendance

attendance_bp = Blueprint("attendance", __name__)

@attendance_bp.get("/scan")
@role_required("manager")
def scan():
    token = request.args.get("token")
    if not token:
        return {"message": "Missing token"}, 400

    payload = decode_qr_payload(token)

    if not payload or "emp" not in payload:
        return {"message": "Invalid QR token"}, 401

    employee_id = payload["emp"]

    employee = mongo.db.employees.find_one({
        "_id": ObjectId(employee_id),
        "is_active": True
    })

    if not employee or "qr_secret" not in employee:
        return {"message": "Invalid employee"}, 401

    verified_payload = verify_qr_token(token, employee["qr_secret"])
    if not verified_payload:
        return {"message": "Invalid or expired QR"}, 401

    try:
        action = scan_attendance(employee_id)
    except ValueError as e:
        return {"message": str(e)}, 400

    return {
        "message": "Scan success",
        "action": action
    }, 200


@attendance_bp.get("/qr")
@role_required("employee", "manager")
def get_qr_token():
    """
    - employee: lấy QR của chính mình
    - manager: truyền ?employee_id= để lấy QR của người khác
    """

    claims = get_jwt()
    role = claims.get("role")
    current_user_id = get_jwt_identity()

    employee_id = request.args.get("employee_id")

    if role == "manager" and not employee_id:
        return {"message": "employee_id is required"}, 400
    
    if role == "employee":
        employee_id = current_user_id


    employee = mongo.db.employees.find_one({
        "_id": to_object_id(employee_id),
        "is_active": True
    })

    if not employee:
        return {"message": "Employee not found"}, 404

    qr_token = generate_qr_token(
        employee_id=str(employee["_id"]),
        secret=employee["qr_secret"]
    )

    return {
        "employee_id": str(employee["_id"]),
        "qr_token": qr_token
    }, 200
