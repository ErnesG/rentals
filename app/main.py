from fastapi import FastAPI
from app.routes import booking, products, invoice, auth, admin
from app.core.exceptions import NotFoundException, DatabaseException
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(DatabaseException)
async def database_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(booking.router, prefix="/bookings", tags=["Bookings"])
app.include_router(invoice.router, prefix="/invoices", tags=["Invoices"])