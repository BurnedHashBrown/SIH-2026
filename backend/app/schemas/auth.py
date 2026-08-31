from pydantic import BaseModel, EmailStr, ConfigDict
from app.utils.constants import UserRole


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserBasicResponse"


class UserBasicResponse(BaseModel):
    id: int
    name: str
    email: str
    employee_id: str
    role: UserRole
    department: str | None = None

    model_config = ConfigDict(from_attributes=True)



TokenResponse.model_rebuild()
