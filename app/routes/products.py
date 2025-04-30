from fastapi import APIRouter, HTTPException
from app.core.database import db
from app.models.product import Product

router = APIRouter()

@router.post("/", response_model=Product)
async def create_product(product: Product):
    result = await db.products.insert_one(product.dict(by_alias=True))
    product.id = str(result.inserted_id)
    return product

@router.get("/", response_model=list[Product])
async def list_products():
    products = await db.products.find().to_list(length=100)
    return products