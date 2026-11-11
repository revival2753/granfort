from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class User(BaseModel):
    username: str = Field(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr

class UserCreate(User):
    password: str = Field(min_length=8, max_length=64, exclude=True)

class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=64, exclude=True)

class UserResponse(User):
    id: int
    is_active: bool = True
    created_at:datetime

model_config = ConfigDict(from_attributes=True)