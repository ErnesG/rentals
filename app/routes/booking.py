from typing import List
from fastapi import APIRouter, HTTPException
from app.models.booking import Booking
from datetime import datetime
from app.core.database import db
from app.services.booking_service import BookingService


router = APIRouter()

@router.post("/", response_model=Booking)
async def create_booking(booking: Booking):
    return await BookingService.create_booking(booking)

@router.get("/{booking_id}", response_model=Booking)
async def get_booking(booking_id: str):
    return await BookingService.get_booking(booking_id)

@router.get("/", response_model=List[Booking])
async def list_bookings():
    return await BookingService.get_bookings()
