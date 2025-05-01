from typing import List
from fastapi import APIRouter, HTTPException
from app.models.booking import Booking
from datetime import datetime
from app.core.database import db


router = APIRouter()

@router.post("/", response_model=Booking)
async def create_booking(booking: Booking):
    
    overlapping = await db.bookings.find_one({"product_id": booking.product_id, "start_date": {"$lte": booking.end_date}, "end_date": {"$gte": booking.start_date}})
    if overlapping:
        raise HTTPException(status_code=400, detail="Booking overlaps with an existing booking")

    result = await db.bookings.insert_one(booking.dict(by_alias=True))
    booking.id = str(result.inserted_id)
    return booking

@router.get("/{booking_id}", response_model=Booking)
async def get_booking(booking_id: str):
    booking = await db.bookings.find_one({"_id": booking_id})
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return Booking(**booking)

@router.get("/", response_model=List[Booking])
async def get_bookings():
    bookings = await db.bookings.find().to_list(length=100)
    return [Booking(**booking) for booking in bookings]
