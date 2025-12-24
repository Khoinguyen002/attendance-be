import os
import hmac
import hashlib
import base64
import json
import time

from app.config import Config

def _get_qr_ttl_seconds() -> int | None:
    """
    QR_TOKEN_TTL:
      - unset / empty / 0  -> vô hạn
      - > 0               -> số giây hết hạn
    """
    ttl = Config.QR_TOKEN_TTL
    if not ttl:
        return None

    try:
        ttl = int(ttl)
        if ttl <= 0:
            return None
        return ttl
    except ValueError:
        return None

def generate_qr_token(employee_id: str, secret: str) -> str:
    ttl = _get_qr_ttl_seconds()
    now = int(time.time())

    payload = {
        "emp": employee_id,
        "iat": now,
    }

    if ttl:
        payload["exp"] = now + ttl

    payload_bytes = json.dumps(
        payload, separators=(",", ":")
    ).encode()

    signature = hmac.new(
        secret.encode(),
        payload_bytes,
        hashlib.sha256
    ).digest()

    token = base64.urlsafe_b64encode(
        payload_bytes + b"." + signature
    ).decode()

    return token

def decode_qr_payload(token: str):
    """
    Decode payload KHÔNG verify chữ ký
    Dùng để lấy employee_id trước
    """
    try:
        raw = base64.urlsafe_b64decode(token.encode())
        payload_bytes, _ = raw.rsplit(b".", 1)
        return json.loads(payload_bytes)
    except Exception:
        return None

def verify_qr_token(token: str, secret: str) -> dict | None:
    try:
        raw = base64.urlsafe_b64decode(token.encode())
        payload_bytes, signature = raw.rsplit(b".", 1)

        expected = hmac.new(
            secret.encode(),
            payload_bytes,
            hashlib.sha256
        ).digest()

        if not hmac.compare_digest(signature, expected):
            return None

        payload = json.loads(payload_bytes)
        now = int(time.time())

        if "exp" in payload and payload["exp"] < now:
            return None

        return payload

    except Exception:
        return None