from typing import Generator
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings
from app.services.product_service import ProductService
from app.services.booking_service import BookingService
from app.services.invoice_service import InvoiceService
from app.services.user_service import UserService
from app.services.admin_service import AdminService

class Container:
    def __init__(self):
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(settings.MONGO_URI)
        self.db: AsyncIOMotorDatabase = self.client[settings.MONGO_DB]
        
        # Initialize services with database dependency
        self.product_service = ProductService(self.db)
        self.booking_service = BookingService(self.db)
        self.invoice_service = InvoiceService(self.db)
        self.user_service = UserService(self.db)
        self.admin_service = AdminService(self.db)

# Create a global container instance
container = Container()

# Dependency injection functions
async def get_product_service() -> ProductService:
    return container.product_service

async def get_booking_service() -> BookingService:
    return container.booking_service

async def get_invoice_service() -> InvoiceService:
    return container.invoice_service

async def get_user_service() -> UserService:
    return container.user_service

async def get_admin_service() -> AdminService:
    return container.admin_service 