from datetime import datetime
from typing import List, Dict
from .base import BaseRepository
from app.core.exceptions import DatabaseException

class AdminRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, "bookings")  # We'll aggregate from bookings collection

    async def get_sales_report(self, start_date: datetime, end_date: datetime) -> Dict:
        try:
            pipeline = [
                {
                    "$match": {
                        "created_at": {
                            "$gte": start_date,
                            "$lte": end_date
                        }
                    }
                },
                {
                    "$lookup": {
                        "from": "invoices",
                        "localField": "id",
                        "foreignField": "booking.id",
                        "as": "invoice"
                    }
                },
                {
                    "$unwind": "$invoice"
                },
                {
                    "$group": {
                        "_id": None,
                        "total_sales": {"$sum": "$invoice.total_amount"},
                        "total_bookings": {"$sum": 1},
                        "average_booking_value": {"$avg": "$invoice.total_amount"}
                    }
                }
            ]
            result = await self.collection.aggregate(pipeline).to_list(length=1)
            return result[0] if result else {"total_sales": 0, "total_bookings": 0, "average_booking_value": 0}
        except Exception as e:
            raise DatabaseException("get_sales_report", str(e))

    async def get_popular_items(self) -> List[Dict]:
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$product_id",
                        "total_bookings": {"$sum": 1}
                    }
                },
                {
                    "$lookup": {
                        "from": "products",
                        "localField": "_id",
                        "foreignField": "_id",
                        "as": "product"
                    }
                },
                {
                    "$unwind": "$product"
                },
                {
                    "$project": {
                        "product_name": "$product.name",
                        "total_bookings": 1,
                        "revenue": {"$multiply": ["$total_bookings", "$product.price_per_day"]}
                    }
                },
                {
                    "$sort": {"total_bookings": -1}
                },
                {
                    "$limit": 10
                }
            ]
            return await self.collection.aggregate(pipeline).to_list(length=10)
        except Exception as e:
            raise DatabaseException("get_popular_items", str(e))

    async def get_availability_report(self) -> List[Dict]:
        try:
            pipeline = [
                {
                    "$lookup": {
                        "from": "products",
                        "localField": "product_id",
                        "foreignField": "_id",
                        "as": "product"
                    }
                },
                {
                    "$unwind": "$product"
                },
                {
                    "$group": {
                        "_id": "$product_id",
                        "product_name": {"$first": "$product.name"},
                        "total_quantity": {"$first": "$product.available_quantity"},
                        "booked_quantity": {"$sum": 1}
                    }
                },
                {
                    "$project": {
                        "product_name": 1,
                        "total_quantity": 1,
                        "booked_quantity": 1,
                        "available_quantity": {
                            "$subtract": ["$total_quantity", "$booked_quantity"]
                        }
                    }
                }
            ]
            return await self.collection.aggregate(pipeline).to_list(length=100)
        except Exception as e:
            raise DatabaseException("get_availability_report", str(e)) 