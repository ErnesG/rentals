from fastapi import FastAPI
from app.routes import booking, products

app = FastAPI()

app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(booking.router, prefix="/bookings", tags=["Bookings"])