from app.core.database import db
from app.models.booking import Booking
from typing import List, Optional
from fastapi import HTTPException

class BookingService:
    @staticmethod
    async def create_booking(booking: Booking) -> Booking:
        result = await db.bookings.insert_one(booking.dict(by_alias=True))
        booking.id = str(result.inserted_id)
        return booking

    @staticmethod
    async def get_booking(booking_id: str) -> Optional[Booking]:
        booking = await db.bookings.find_one({"_id": booking_id})
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        return Booking(**booking)

    @staticmethod
    async def get_bookings() -> List[Booking]:
        bookings = await db.bookings.find().to_list(length=100)
        return [Booking(**booking) for booking in bookings] 