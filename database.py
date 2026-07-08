# =============================================================================
#  database.py - Database Configuration & Connection Setup
#  Project 2: Database Integration (CRUD)
# =============================================================================

# SQLAlchemy provides the ORM engine and session factory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -----------------------------------------------------------------------------
# Database URL Configuration
# -----------------------------------------------------------------------------
# Using SQLite for simplicity (file-based, no server needed)
# In production, you'd use PostgreSQL: postgresql://user:pass@localhost/dbname
DATABASE_URL = "sqlite:///./users.db"

# -----------------------------------------------------------------------------
# Create the SQLAlchemy Engine
# -----------------------------------------------------------------------------
# check_same_thread=False is required for SQLite to work with FastAPI
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True   # Set to False in production to hide SQL logs
)

# -----------------------------------------------------------------------------
# Create a Session Factory
# -----------------------------------------------------------------------------
# Each request will get its own database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -----------------------------------------------------------------------------
# Base Class for ORM Models
# -----------------------------------------------------------------------------
# All our models will inherit from this Base class
Base = declarative_base()

# -----------------------------------------------------------------------------
# Dependency: Get DB Session
# -----------------------------------------------------------------------------
# This function is called for every request, providing a fresh DB session
# and ensuring it's properly closed when the request is done.
def get_db():
    db = SessionLocal()
    try:
        yield db   # Provide the session to the route
    finally:
        db.close() # Always close after the request completes
