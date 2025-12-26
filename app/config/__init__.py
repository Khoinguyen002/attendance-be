from datetime import timedelta
import os

class Config:
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    PORT = int(os.getenv("PORT", 5000))
    CORS_ORIGINS = [
        "http://localhost:5173",
        "https://attendance-fe.pages.dev",
    ]

    CORS_SUPPORTS_CREDENTIALS = True

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", 30))
    )

    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb://localhost:27017/attendance"
    )
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "attendance")

    QR_TOKEN_TTL = int(os.getenv("QR_TOKEN_TTL", "0"))

    TIMEZONE = os.getenv("TIMEZONE", "Asia/Ho_Chi_Minh")
    WORK_START = os.getenv("WORK_START", "08:30")
    WORK_END = os.getenv("WORK_END", "17:30")