from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.booking import Booking
from typing import List, Optional
from fastapi import HTTPException

class BookingService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create_booking(self, booking: Booking) -> Booking:
        result = await self.db.bookings.insert_one(booking.dict(by_alias=True))
        booking.id = str(result.inserted_id)
        return booking

    async def get_booking(self, booking_id: str) -> Optional[Booking]:
        booking = await self.db.bookings.find_one({"_id": booking_id})
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        return Booking(**booking)

    async def get_bookings(self) -> List[Booking]:
        bookings = await self.db.bookings.find().to_list(length=100)
        return [Booking(**booking) for booking in bookings] 