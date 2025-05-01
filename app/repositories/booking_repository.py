from app.models.booking import Booking
from .base import BaseRepository

class BookingRepository(BaseRepository[Booking]):
    def __init__(self, db):
        super().__init__(db, "bookings") 