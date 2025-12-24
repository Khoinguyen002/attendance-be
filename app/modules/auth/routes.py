# app/modules/auth/routes.py
from flask import Blueprint, request

from app.modules.auth.service import authenticate

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/login")
def login():
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return {"message": "Email and password are required"}, 400

    result = authenticate(
        email=data["email"],
        password=data["password"]
    )

    if not result:
        return {"message": "Invalid credentials"}, 401

    return result, 200
