from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from app.models.product import Product
from app.models.booking import Booking
class InvoiceItem(BaseModel):
    product: Product
    quantity: int
    total_days: int
    sub_total: float

    @classmethod
    def from_product(cls, booking: Booking, product: Product):
        return cls(
            product=product,
            quantity= booking.quantity,
            total_days=booking.end_date - booking.start_date,
            sub_total=product.price_per_day *(booking.end_date - booking.start_date)
        )
    
