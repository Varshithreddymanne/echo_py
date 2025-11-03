from jose import jwt, JWTError
from datetime import datetime, timedelta
import os

SECRET = os.getenv("JWT_SECRET")
ALGO = os.getenv("JWT_ALGORITHM", "HS256")

def create_access_token(data: dict, expires_minutes: int = 60*6):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET, algorithm=ALGO)
    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        return payload
    except JWTError:
        return None