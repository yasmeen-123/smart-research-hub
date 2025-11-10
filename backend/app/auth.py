from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
import os

# --- Environment Variables ---
SECRET_KEY = os.getenv("JWT_SECRET", "secret-dev-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# --- Password Hashing Context ---
# bcrypt_sha256 avoids the 72-byte password limit safely
pwd_context = CryptContext(
    schemes=["bcrypt_sha256"],
    deprecated="auto"
)

# --- Password Hashing ---
def hash_password(password: str) -> str:
    """Return a secure hash for the provided password."""
    try:
        return pwd_context.hash(password)
    except Exception as e:
        print(f"[AUTH] Error hashing password: {e}")
        raise

def verify_password(password: str, hashed_password: str) -> bool:
    """Validate a password against its stored hash."""
    try:
        return pwd_context.verify(password, hashed_password)
    except Exception as e:
        print(f"[AUTH] Error verifying password: {e}")
        raise

# --- Token Management ---
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode["exp"] = expire
    try:
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        print(f"[AUTH] Error creating token: {e}")
        raise

def decode_token(token: str) -> dict | None:
    """Decode a JWT token and return its payload, or None if invalid."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        print(f"[AUTH] Error decoding token: {e}")
        return None
