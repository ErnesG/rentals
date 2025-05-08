from fastapi import APIRouter, Depends
from app.models.invoice import Invoice
from app.services.invoice_service import InvoiceService
from app.services.booking_service import BookingService
from app.core.container import get_invoice_service, get_booking_service
from typing import List

router = APIRouter()

@router.post("/generate/{booking_id}", response_model=Invoice)
async def generate_invoice(
    booking_id: str,
    invoice_service: InvoiceService = Depends(get_invoice_service),
    booking_service: BookingService = Depends(get_booking_service)
):
    booking = await booking_service.get_booking(booking_id)
    return await invoice_service.generate_invoice(booking)

# ... rest of the routes remain the same ... 