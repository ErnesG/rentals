from fastapi import APIRouter, Depends
from typing import List, Dict
from datetime import datetime
from app.core.auth import get_current_admin
from app.models.user import User
from app.services.admin_service import AdminService
from app.core.container import get_admin_service

router = APIRouter()

@router.get("/reports/sales", dependencies=[Depends(get_current_admin)])
async def sales_report(
    start_date: datetime,
    end_date: datetime,
    admin_service: AdminService = Depends(get_admin_service)
) -> Dict:
    return await admin_service.get_sales_report(start_date, end_date)

@router.get("/reports/popular-items", dependencies=[Depends(get_current_admin)])
async def popular_items(
    admin_service: AdminService = Depends(get_admin_service)
) -> List[Dict]:
    return await admin_service.get_popular_items()

@router.get("/reports/availability", dependencies=[Depends(get_current_admin)])
async def availability_report(
    admin_service: AdminService = Depends(get_admin_service)
) -> List[Dict]:
    return await admin_service.get_availability_report()
