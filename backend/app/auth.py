from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
from typing import Optional, Dict, Any, Union

SECRET_KEY = os.getenv("JWT_SECRET", "secret-dev-key")
ALGORITHM = "HS256"
# Safely cast the env var to int, defaulting to 1 day (60 * 24)
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))
except ValueError:
    ACCESS_TOKEN_EXPIRE_MINUTES = 1440
    print("[AUTH] Warning: ACCESS_TOKEN_EXPIRE_MINUTES is not a valid integer. Using default (1440).")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Switched to 'bcrypt' as it's more common than 'bcrypt_sha256' in passlib


def hash_password(password: str) -> str:
    """Hashes a plaintext password."""
    # Rely on passlib to handle errors, as an error here is critical.
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies a plaintext password against a hash."""
    # Rely on passlib to handle errors.
    return pwd_context.verify(password, hashed_password)


def create_access_token(
    data: Dict[str, Union[str, int]],
    expires_delta: Optional[timedelta] = None
) -> str:
    """Creates a JWT access token."""
    to_encode = data.copy()
    
    # Calculate expiration time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode["exp"] = expire
    
    # Use 'sub' key for the main identity (standard JWT claim)
    if "sub" not in to_encode:
        print("[AUTH] Warning: Token data is missing the 'sub' claim.")
        
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """Decodes a JWT token, returning the payload or None if invalid/expired."""
    try:
        # The return is explicitly Optional[Dict[str, Any]] to match FastAPI expectations
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        # JWTError covers all token-related failures (expired, invalid signature, etc.)
        return None