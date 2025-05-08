from fastapi import APIRouter, Depends
from typing import List
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/reports/sales")
async def sales_report(
    start_date: datetime,
    end_date: datetime,
    admin_service: AdminService = Depends(get_admin_service)
):
    return await admin_service.get_sales_report(start_date, end_date)

@router.get("/reports/popular-items")
async def popular_items():
    pass

@router.get("/reports/availability")
async def availability_report():
    pass
