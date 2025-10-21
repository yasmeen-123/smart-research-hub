from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
import os

# --- Environment Variables ---
SECRET_KEY = os.getenv("JWT_SECRET", "secret-dev-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# --- Password Hashing Context ---
pwd_context = CryptContext(
    schemes=["bcrypt_sha256"],  # Handles passwords longer than 72 bytes safely
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """Return a secure hash for the provided password."""
    try:
        return pwd_context.hash(password)
    except Exception as e:
        print(f"Error hashing password: {str(e)}")
        raise


def verify_password(password: str, hashed_password: str) -> bool:
    """Validate a password against its stored hash."""
    try:
        return pwd_context.verify(password, hashed_password)
    except Exception as e:
        print(f"Error verifying password: {str(e)}")
        raise


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)
    expire += expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    try:
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        print(f"Error creating token: {str(e)}")
        raise


def decode_token(token: str) -> dict | None:
    """Decode a JWT token and return its payload, or None if invalid."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        print(f"Error decoding token: {str(e)}")
        return None