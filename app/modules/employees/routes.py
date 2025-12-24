from flask import Blueprint, request
from bson import ObjectId

from app.common.decorators import role_required
from app.modules.employees.service import (
    create_employee,
    list_employees,
    get_employee,
    update_employee,
    disable_employee
)

employee_bp = Blueprint("employees", __name__)


@employee_bp.post("/")
@role_required("manager")
def create():
    data = request.get_json()
    if not data:
        return {"message": "Invalid body"}, 400

    try:
        emp = create_employee(data)
    except ValueError as e:
        return {"message": str(e)}, 400

    return {
        "id": str(emp["_id"]),
        "email": emp["email"],
        "name": emp["name"],
        "role": emp["role"]
    }, 201


@employee_bp.get("/")
@role_required("manager")
def list_all():
    employees = list_employees()
    for e in employees:
        e["_id"] = str(e["_id"])
    return employees, 200


@employee_bp.get("/<emp_id>")
@role_required("manager")
def detail(emp_id):
    emp = get_employee(emp_id)
    if not emp:
        return {"message": "Employee not found"}, 404

    emp["_id"] = str(emp["_id"])
    return emp, 200


@employee_bp.put("/<emp_id>")
@role_required("manager")
def update(emp_id):
    data = request.get_json()
    if not data:
        return {"message": "Invalid body"}, 400

    try:
        update_employee(emp_id, data)
    except ValueError as e:
        return {"message": str(e)}, 400

    return {"message": "Updated"}, 200


@employee_bp.delete("/<emp_id>")
@role_required("manager")
def delete(emp_id):
    disable_employee(emp_id)
    return {"message": "Disabled"}, 200
