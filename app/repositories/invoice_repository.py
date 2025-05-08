from app.models.invoice import Invoice
from .base import BaseRepository
from app.core.exceptions import NotFoundException, DatabaseException

class InvoiceRepository(BaseRepository[Invoice]):
    def __init__(self, db):
        super().__init__(db, "invoices")

    async def get_by_booking_id(self, booking_id: str):
        try:
            result = await self.collection.find_one({"booking.id": booking_id})
            if not result:
                raise NotFoundException("Invoice", f"with booking_id {booking_id}")
            return result
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException("get_by_booking_id", str(e))

    async def update_status(self, invoice_id: str, status: str):
        try:
            result = await self.collection.update_one(
                {"_id": invoice_id},
                {"$set": {"status": status}}
            )
            if result.modified_count == 0:
                raise NotFoundException("Invoice", invoice_id)
            return await self.get_by_id(invoice_id)
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException("update_status", str(e)) 