from fastapi import APIRouter
from app.models.product import Product
from app.services.product_service import ProductService

router = APIRouter()

@router.post("/", response_model=Product)
async def create_product(product: Product):
    return await ProductService.create_product(product)

@router.get("/", response_model=list[Product])
async def list_products():
    return await ProductService.get_products()