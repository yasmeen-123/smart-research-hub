import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from typing import Generator
from sqlalchemy.orm import Session
from pathlib import Path # Used for cleaner path handling

# --- Configuration ---
load_dotenv() 

# 💡 FIX: Use an absolute path for the SQLite database file

# Get the directory where this db.py file resides
BASE_DIR = Path(__file__).resolve().parent

# Define the database file name (can be set in .env or defaults to a safe name)
DB_FILE_NAME = os.getenv("DB_FILE_NAME", "smart_research_hub.db") 

# Construct the absolute path to the database file
DB_PATH = BASE_DIR / DB_FILE_NAME

# The final SQLAlchemy URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}" 


# --- Engine Setup ---
# For SQLite, we need this argument to allow multiple threads (requests) 
# to interact with the database connection.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

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