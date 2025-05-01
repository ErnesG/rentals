from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.product import Product
from typing import List

class ProductService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create_product(self, product: Product) -> Product:
        result = await self.db.products.insert_one(product.dict(by_alias=True))
        product.id = str(result.inserted_id)
        return product

    async def get_products(self) -> List[Product]:
        products = await self.db.products.find().to_list(length=100)
        return [Product(**product) for product in products] 