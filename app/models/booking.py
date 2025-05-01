from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId

class Booking(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()))
    product_id: str
    start_date: datetime
    end_date: datetime
    status: str = "pending"
    delivery_address: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        
