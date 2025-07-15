# main.py
# FastAPI app for user profile update and retrieval with custom validation and structured error handling

from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, EmailStr, validator, ValidationError, root_validator
from typing import Optional, Dict

app = FastAPI()

# --- In-memory user data store (user_id: profile) --- #
user_db: Dict[str, Dict] = {
    "user1": {
        "name": "Alice",
        "email": "alice@example.com",
        "age": 29,
        "bio": "Backend developer."
    },
    "user2": {
        "name": "Bob",
        "email": "bob@example.com",
        "age": 42,
        "bio": "DevOps engineer."
    },
}

# --- Dummy current_user dependency (returns a mock user) --- #
def get_current_user():
    # For this assessment, we'll use 'user1' for authenticated requests
    return {"username": "user1"}

# --- Profile models --- #
class ProfileResponse(BaseModel):
    name: str
    email: EmailStr
    age: int
    bio: Optional[str] = None

class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    bio: Optional[str] = None

    @validator("age")
    def age_must_be_valid(cls, v):
        if v is not None and not (18 <= v <= 120):
            raise ValueError("age must be between 18 and 120")
        return v

    @validator("email")
    def email_format_valid(cls, v):
        # EmailStr already performs basic validation
        return v

class CustomValidationException(Exception):
    def __init__(self, errors):
        self.errors = errors

# --- Custom exception handler for input validation errors --- #
@app.exception_handler(CustomValidationException)
async def custom_validation_exception_handler(request: Request, exc: CustomValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors
        }
    )

# Override FastAPI's default validation error handling for pydantic validation (body)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

# --- Profile retrieval endpoint --- #
@app.get("/user/profile", response_model=ProfileResponse)
def get_profile(current_user: dict = Depends(get_current_user)):
    """
    Retrieve the authenticated user's profile.
    """
    user_id = current_user["username"]
    profile = user_db.get(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile

# --- Profile update endpoint --- #
@app.put("/user/profile", response_model=ProfileResponse)
def update_profile(
    update: ProfileUpdateRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Update the authenticated user's profile. Fields are optional (partial update).

    # Testing instructions/examples:
    #   - Update email and age:
    #       curl -X PUT http://localhost:8000/user/profile -H "Content-Type: application/json" -d '{"email": "alice.new@example.com", "age": 34}'
    #   - Send invalid age:
    #       curl -X PUT http://localhost:8000/user/profile -H "Content-Type: application/json" -d '{"age": 15}'
    #   - Send invalid email:
    #       curl -X PUT http://localhost:8000/user/profile -H "Content-Type: application/json" -d '{"email": "bademail"}'
    """
    user_id = current_user["username"]
    profile = user_db.get(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    errors = []
    # Validate fields manually for custom logic (Pydantic validators catch most cases)
    try:
        update_dict = update.dict(exclude_unset=True)
        _ = ProfileUpdateRequest(**update_dict)  # Triggers field-level Pydantic validators
    except ValidationError as ve:
        # Convert Pydantic's error format to custom format
        for err in ve.errors():
            errors.append({
                "loc": err["loc"],
                "msg": err["msg"],
                "type": err["type"]
            })
        raise CustomValidationException(errors)
    # Apply changes for provided fields only
    for k, v in update_dict.items():
        profile[k] = v
    user_db[user_id] = profile
    return profile
