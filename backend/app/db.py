import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from typing import Generator
from sqlalchemy.orm import Session # Required for type hinting

# --- Configuration ---
load_dotenv() 

# 💡 FIX: Use DATABASE_URL from environment, defaulting to local SQLite
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./smart_research_hub.db" # Defaulting to a more descriptive name
)

# --- Engine Setup ---
# For SQLite, we need this argument to allow multiple threads (requests) 
# to interact with the database connection.
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

# --- Session Setup ---
# SessionLocal is the factory for creating new Session objects
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# Base class for models
Base = declarative_base()


# --- Dependency Function ---
def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session for a single request 
    and ensures it is closed afterwards.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        # Ensures the database session is always closed
        db.close()