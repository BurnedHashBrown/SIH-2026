from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from app.utils.constants import UserRole


class UserBase(BaseModel):
    name: str
    email: EmailStr
    employee_id: str
    role: UserRole = UserRole.INSPECTOR
    department: str | None = "Legal Metrology Department"
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    role: UserRole | None = None
    department: str | None = None
    is_active: bool | None = None
    password: str | None = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

