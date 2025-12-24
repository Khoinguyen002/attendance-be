import os

class Config:
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    PORT = int(os.getenv("PORT", 5000))

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret")

    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb://localhost:27017/attendance"
    )
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "attendance")

    QR_TOKEN_TTL = int(os.getenv("QR_TOKEN_TTL", "0"))
    QR_SCAN_COOLDOWN = int(os.getenv("QR_SCAN_COOLDOWN", "60"))
