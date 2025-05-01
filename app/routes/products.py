from fastapi import APIRouter, Depends
from app.models.product import Product
from app.services.product_service import ProductService
from app.core.container import get_product_service

router = APIRouter()

@router.post("/", response_model=Product)
async def create_product(
    product: Product,
    product_service: ProductService = Depends(get_product_service)
):
    return await product_service.create_product(product)

@router.get("/", response_model=list[Product])
async def list_products(
    product_service: ProductService = Depends(get_product_service)
):
    return await product_service.get_products()