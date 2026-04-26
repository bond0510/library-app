from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional


class MemberCreate(BaseModel):
    name: str = Field(..., example="John Doe")
    email: EmailStr = Field(..., example="john@example.com")  # validation
    phone: str = Field(..., example="9876543210")


class MemberUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[str] = None


class MemberResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    status: str

    model_config = ConfigDict(from_attributes=True)