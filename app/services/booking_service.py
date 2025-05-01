from typing import List
from app.models.booking import Booking
from app.repositories.booking_repository import BookingRepository
from motor.motor_asyncio import AsyncIOMotorDatabase

class BookingService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repository = BookingRepository(db)

    async def create_booking(self, booking: Booking) -> Booking:
        return await self.repository.create(booking)

    async def get_booking(self, booking_id: str) -> Booking:
        booking = await self.repository.get_by_id(booking_id)
        return Booking(**booking)

    async def get_bookings(self) -> List[Booking]:
        bookings = await self.repository.get_all()
        return [Booking(**booking) for booking in bookings] 