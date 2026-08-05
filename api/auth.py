import os
import json
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from dotenv import load_dotenv
import bcrypt

from database.core.storage.base_pool import DatabasePool
from api.deps import get_db_pool, limiter

load_dotenv()

router = APIRouter(prefix="/auth", tags=["authentication"])

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# ---------- Password helpers using bcrypt ----------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# ---------- Models ----------
class User(BaseModel):
    id: int
    username: str
    role: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

# ---------- Helper functions ----------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire, "refresh": True})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_user(db_pool: DatabasePool, username: str):
    row = db_pool.fetch_one("SELECT id, username, hashed_password, role FROM users WHERE username = %s", (username,))
    if row:
        return dict(row)
    return None

async def authenticate_user(db_pool: DatabasePool, username: str, password: str):
    user = await get_user(db_pool, username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

# ---------- Current user dependencies ----------
async def get_current_user(token: str = Depends(oauth2_scheme), db_pool: DatabasePool = Depends(get_db_pool)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        role: str = payload.get("role")
    except JWTError:
        raise credentials_exception
    user = await get_user(db_pool, username)  # <-- added await
    if user is None:
        raise credentials_exception
    return User(id=user["id"], username=user["username"], role=user["role"])

def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user

# ---------- Login endpoint with rate limiting ----------
@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_pool: DatabasePool = Depends(get_db_pool),
):
    user = await authenticate_user(db_pool, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    refresh_token = create_refresh_token(data={"sub": user["username"], "role": user["role"]})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

# ---------- Refresh token ----------
@router.post("/refresh", response_model=Token)
async def refresh_token(request: Request, db_pool: DatabasePool = Depends(get_db_pool)):
    data = await request.json()
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if not payload.get("refresh"):
            raise JWTError
        username = payload.get("sub")
        if not username:
            raise JWTError
        user = await get_user(db_pool, username)
        if not user:
            raise JWTError
        access_token = create_access_token(data={"sub": username, "role": user["role"]})
        new_refresh = create_refresh_token(data={"sub": username, "role": user["role"]})
        return {"access_token": access_token, "refresh_token": new_refresh, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

# ---------- Create users table and admin user ----------
def create_users_table(db_pool: DatabasePool = None):
    """Create the users table if it doesn't exist, and insert admin user."""
    from api.main import app
    pool = db_pool or app.state.db_pool

    # Check if table exists
    try:
        pool.fetch_one("SELECT 1 FROM users LIMIT 1")
        # table exists, but we still need to ensure admin user exists
    except Exception:
        # Create table
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            role VARCHAR(20) NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
        """
        pool.execute_query(query)

    # Insert admin user if not present
    admin_pass = os.getenv("INITIAL_ADMIN_PASSWORD", "admin123")
    hashed = get_password_hash(admin_pass)
    pool.execute_query(
        "INSERT INTO users (username, hashed_password, role) VALUES (%s, %s, %s) ON CONFLICT (username) DO NOTHING",
        ("admin", hashed, "admin")
    )
