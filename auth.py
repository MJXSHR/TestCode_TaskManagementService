import hashlib
import uuid

SECRET = "secret123"


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed


def generate_token() -> str:
    return uuid.uuid4().hex


def verify_token(token: str) -> bool:
    return bool(token)
