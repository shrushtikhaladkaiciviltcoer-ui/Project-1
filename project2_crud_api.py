# =============================================================================
#  Project 2: Database Integration (CRUD)
#  Framework  : FastAPI + SQLAlchemy ORM
#  Database   : SQLite (file-based, persistent)
#  Model      : User with email, age, is_active, created_at
# =============================================================================

# ----------------------------- 1. IMPORTS ------------------------------------
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Session
from typing import Optional

# Import the database configuration from our other file
from database import Base, engine, get_db

# =============================================================================
# =================== ORM MODEL (DATABASE SCHEMA) ============================
# =============================================================================

class User(Base):
    """
    SQLAlchemy ORM Model for the 'users' table.
    
    Schema:
        id         : Auto-incrementing primary key
        email      : Unique string (enforces no duplicates at DB level)
        age        : Integer (must be >= 0, enforced at app level)
        is_active  : Boolean (defaults to TRUE)
        created_at : UTC timestamp (audit trail)
    """
    __tablename__ = "users"
    
    # Primary Key: System-assigned unique ID
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Email: Unique constraint prevents duplicate registrations
    email = Column(String(255), unique=True, index=True, nullable=False)
    
    # Age: Integer, validated in Pydantic schema
    age = Column(Integer, nullable=False)
    
    # State Flag: Boolean, defaults to TRUE
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Audit Trail: UTC timestamp for record creation
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

# Create all tables in the database (runs once on startup)
Base.metadata.create_all(bind=engine)

# =============================================================================
# =================== PYDANTIC SCHEMAS (VALIDATION) ==========================
# =============================================================================

class UserCreate(BaseModel):
    """
    Schema for creating a new user (POST request body).
    Validates incoming data BEFORE it touches the database.
    """
    email: EmailStr  # Auto-validates email format (requires email-validator)
    age: int = Field(..., ge=0, description="Age must be 0 or greater")
    
    @field_validator('age')
    @classmethod
    def validate_age(cls, v):
        """Custom validation: age must be non-negative"""
        if v < 0:
            raise ValueError("Age must be greater than or equal to 0")
        return v

class UserUpdate(BaseModel):
    """
    Schema for updating an existing user (PUT request body).
    All fields are optional - only provided fields will be updated.
    """
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    """
    Schema for user data in responses (GET/POST output).
    """
    id: int
    email: str
    age: int
    is_active: bool
    created_at: datetime
    
    # Tells Pydantic to read data from SQLAlchemy model attributes
    class Config:
        from_attributes = True

# =============================================================================
# ======================== FASTAPI APPLICATION ================================
# =============================================================================

app = FastAPI(
    title="User CRUD API",
    description="Project 2: Database Integration with FastAPI + SQLAlchemy",
    version="1.0.0"
)

# =============================================================================
# =========================== ROOT ENDPOINT ===================================
# =============================================================================

@app.get("/", tags=["Root"])
def read_root():
    """Welcome endpoint - health check"""
    return {
        "message": "🗄️ User CRUD API is running",
        "framework": "FastAPI + SQLAlchemy",
        "endpoints": {
            "POST   /users":       "Create a new user",
            "GET    /users":       "Get all users",
            "GET    /users/{id}":  "Get a single user by ID",
            "PUT    /users/{id}":  "Update a user",
            "DELETE /users/{id}":  "Delete a user"
        }
    }

# =============================================================================
# ======================== CREATE - POST /users ===============================
# =============================================================================

@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    CREATE operation: Register a new user in the database.
    
    Logic Flow:
        1. Receive and validate JSON body (Pydantic)
        2. Check if email already exists (duplicate prevention)
        3. If unique, create the new user record
        4. Return 201 Created with the new user data
    """
    # ------------------------------------------------------------------
    # Step 1: Check for duplicate email
    # ------------------------------------------------------------------
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{user.email}' already exists"
        )
    
    # ------------------------------------------------------------------
    # Step 2: Create the new user object
    # ------------------------------------------------------------------
    new_user = User(
        email=user.email,
        age=user.age,
        is_active=True   # Default state flag
    )
    
    # ------------------------------------------------------------------
    # Step 3: Save to database
    # ------------------------------------------------------------------
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Refresh to get the auto-generated ID and timestamp
    
    # Return 201 Created with the new user
    return new_user

# =============================================================================
# ======================== READ ALL - GET /users ==============================
# =============================================================================

@app.get("/users", response_model=list[UserResponse], tags=["Users"])
def get_all_users(db: Session = Depends(get_db)):
    """
    READ operation: Retrieve all users from the database.
    
    Returns:
        200 OK with a list of all users
    """
    users = db.query(User).all()
    return users

# =============================================================================
# ======================= READ ONE - GET /users/{id} ==========================
# =============================================================================

@app.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    READ operation: Retrieve a single user by their ID.
    
    Returns:
        200 OK with user data
        404 Not Found if user doesn't exist
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    return user

# =============================================================================
# ======================== UPDATE - PUT /users/{id} ===========================
# =============================================================================

@app.put("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    UPDATE operation: Modify an existing user's information.
    
    Logic Flow:
        1. Find the user by ID
        2. If email is being changed, check it's not taken by another user
        3. Apply only the fields that were provided
        4. Save changes and return updated user
    """
    # ------------------------------------------------------------------
    # Step 1: Find the user
    # ------------------------------------------------------------------
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    # ------------------------------------------------------------------
    # Step 2: If updating email, check for duplicates
    # ------------------------------------------------------------------
    if user_update.email and user_update.email != user.email:
        duplicate = db.query(User).filter(User.email == user_update.email).first()
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email '{user_update.email}' is already taken by another user"
            )
        user.email = user_update.email
    
    # ------------------------------------------------------------------
    # Step 3: Update other fields if provided
    # ------------------------------------------------------------------
    if user_update.age is not None:
        user.age = user_update.age
    
    if user_update.is_active is not None:
        user.is_active = user_update.is_active
    
    # ------------------------------------------------------------------
    # Step 4: Save changes
    # ------------------------------------------------------------------
    db.commit()
    db.refresh(user)
    
    return user

# =============================================================================
# ======================== DELETE - DELETE /users/{id} ========================
# =============================================================================

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    DELETE operation: Permanently remove a user from the database.
    
    Returns:
        204 No Content on successful deletion
        404 Not Found if user doesn't exist
    """
    # ------------------------------------------------------------------
    # Step 1: Find the user
    # ------------------------------------------------------------------
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    # ------------------------------------------------------------------
    # Step 2: Delete the user
    # ------------------------------------------------------------------
    db.delete(user)
    db.commit()
    
    # 204 No Content - successful deletion, no body to return
    return None

# =============================================================================
# =========================== SERVER STARTUP ==================================
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🗄️  Starting User CRUD API Server")
    print("=" * 60)
    print("📡 Base URL: http://127.0.0.1:8000")
    print("📖 Docs URL: http://127.0.0.1:8000/docs")
    print("=" * 60)
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
