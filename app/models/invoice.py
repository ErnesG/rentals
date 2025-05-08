from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from app.models.booking import Booking
from app.models.Invoice_item import InvoiceItem
from app.models.product import Product
class Invoice(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()))
    booking: Booking
    total_amount: float
    created_at: datetime = datetime.now()
    status: str = "pending"

    @classmethod
    def from_booking(cls, booking:Booking, product: Product):
        item = InvoiceItem.from_product(booking, product)
        return cls(
            booking=booking,
            total_amount = item.sub_total,
            items = [item]
        )
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

