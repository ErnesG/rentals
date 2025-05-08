from datetime import datetime
from typing import List, Dict
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.admin_repository import AdminRepository
from app.models.booking import Booking
from app.models.product import Product

class AdminService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repository = AdminRepository(db)

    async def get_sales_report(self, start_date: datetime, end_date: datetime) -> Dict:
        return await self.repository.get_sales_report(start_date, end_date)

    async def get_popular_items(self) -> List[Dict]:
        return await self.repository.get_popular_items()

    async def get_availability_report(self) -> List[Dict]:
        return await self.repository.get_availability_report() 