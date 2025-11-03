from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from app.database import db
from app.models import UserCreate, UserLogin
from app.utils import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register(user: UserCreate):
    existing_email = await db.users.find_one({"email": user.email})
    existing_user = await db.users.find_one({"username": user.username})
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = pwd_ctx.hash(user.password)
    await db.users.insert_one({
        "username": user.username,
        "email": user.email,
        "password": hashed,
    })
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(data: UserLogin):
    user = await db.users.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not pwd_ctx.verify(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"email": user["email"], "username": user["username"]})
    return {"access_token": token}


