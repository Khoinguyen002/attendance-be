import bcrypt
from flask_jwt_extended import create_access_token
from app.extensions.mongo import mongo


def authenticate(email: str, password: str):
    user = mongo.db.employees.find_one(
        {"email": email, "is_active": True}
    )

    if not user:
        return None

    if not bcrypt.checkpw(
        password.encode("utf-8"),
        user["password"].encode("utf-8")
    ):
        return None

    access_token = create_access_token(
        identity=str(user["_id"]),
        additional_claims={
            "role": user["role"],
            "email": user["email"]
        }
    )

    return {
        "access_token": access_token,
        "user": {
            "id": str(user["_id"]),
            "email": user["email"],
            "name": user["name"],
            "role": user["role"]
        }
    }
