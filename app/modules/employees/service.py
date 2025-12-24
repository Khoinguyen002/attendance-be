import bcrypt
import secrets
from datetime import datetime
from bson import ObjectId

from app.extensions.mongo import mongo


def create_employee(data: dict):
    if mongo.db.employees.find_one({"email": data["email"]}):
        raise ValueError("Email already exists")

    hashed = bcrypt.hashpw(
        data["password"].encode(),
        bcrypt.gensalt()
    ).decode()

    employee = {
        "email": data["email"],
        "password": hashed,
        "name": data["name"],
        "role": data.get("role", "employee"),
        "qr_secret": secrets.token_urlsafe(32),
        "is_active": True,
        "created_at": datetime.utcnow()
    }

    mongo.db.employees.insert_one(employee)
    return employee


def list_employees():
    return list(
        mongo.db.employees.find(
            {"is_active": True},
            {"password": 0, "qr_secret": 0}
        )
    )


def get_employee(emp_id: str):
    return mongo.db.employees.find_one(
        {"_id": ObjectId(emp_id), "is_active": True},
        {"password": 0, "qr_secret": 0}
    )


def update_employee(emp_id: str, data: dict):
    update = {}

    if "name" in data:
        update["name"] = data["name"]

    if "role" in data:
        update["role"] = data["role"]

    if "password" in data:
        update["password"] = bcrypt.hashpw(
            data["password"].encode(),
            bcrypt.gensalt()
        ).decode()

    if not update:
        raise ValueError("No valid fields to update")

    mongo.db.employees.update_one(
        {"_id": ObjectId(emp_id)},
        {"$set": update}
    )


def disable_employee(emp_id: str):
    mongo.db.employees.update_one(
        {"_id": ObjectId(emp_id)},
        {"$set": {"is_active": False}}
    )

def hard_delete_employee(emp_id: str):
    result = mongo.db.employees.delete_one(
        {"_id": ObjectId(emp_id)}
    )

    if result.deleted_count == 0:
        raise ValueError("Employee not found")
