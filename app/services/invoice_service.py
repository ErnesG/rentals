from typing import List
from app.models.invoice import Invoice, InvoiceItem
from app.models.booking import Booking
from app.repositories.invoice_repository import InvoiceRepository
from app.services.product_service import ProductService
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

class InvoiceService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repository = InvoiceRepository(db)
        self.product_service = ProductService(db)

    async def generate_invoice(self, booking: Booking) -> Invoice:
        # Get product details
        product = await self.product_service.get_product(booking.product_id)
        
        # Create invoice directly from booking
        invoice = await Invoice.from_booking(booking, product)
        
        return await self.repository.create(invoice)

    async def get_invoice(self, invoice_id: str) -> Invoice:
        invoice = await self.repository.get_by_id(invoice_id)
        return Invoice(**invoice)

    async def get_invoice_by_booking(self, booking_id: str) -> Invoice:
        invoice = await self.repository.get_by_booking_id(booking_id)
        return Invoice(**invoice)

    async def get_all_invoices(self) -> List[Invoice]:
        invoices = await self.repository.get_all()
        return [Invoice(**invoice) for invoice in invoices] 