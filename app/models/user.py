from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId

class User(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()))
    email: EmailStr
    full_name: str
    password: str  # Should be hashed
    role: str = "customer"  # admin or customer
    phone: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
