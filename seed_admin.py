# seed_admin.py
import bcrypt
from pymongo import MongoClient

ADMIN_EMAIL = "admin@company.com"
ADMIN_PASSWORD = "123456"

client = MongoClient("mongodb://localhost:27017")
db = client.attendance

hashed_password = bcrypt.hashpw(
    ADMIN_PASSWORD.encode("utf-8"),
    bcrypt.gensalt()
).decode("utf-8")

db.employees.insert_one({
    "email": ADMIN_EMAIL,
    "password": hashed_password,
    "name": "Admin",
    "role": "manager",
    "is_active": True
})

print("Admin user created")
