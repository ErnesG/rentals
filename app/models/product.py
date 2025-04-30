from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class Product(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    description: Optional[str] = None
    type: str
    price_per_day: float
    available_quantity: int
    image_url: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}