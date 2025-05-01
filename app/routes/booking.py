from typing import List
from fastapi import APIRouter, HTTPException, Depends
from app.models.booking import Booking
from datetime import datetime
from app.services.booking_service import BookingService
from app.core.container import get_booking_service


router = APIRouter()

@router.post("/", response_model=Booking)
async def create_booking(
    booking: Booking,
    booking_service: BookingService = Depends(get_booking_service)
):
    return await booking_service.create_booking(booking)

@router.get("/{booking_id}", response_model=Booking)
async def get_booking(
    booking_id: str,
    booking_service: BookingService = Depends(get_booking_service)
):
    return await booking_service.get_booking(booking_id)

@router.get("/", response_model=List[Booking])
async def list_bookings(
    booking_service: BookingService = Depends(get_booking_service)
):
    return await booking_service.get_bookings()
