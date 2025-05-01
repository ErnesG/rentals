from typing import List
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from motor.motor_asyncio import AsyncIOMotorDatabase

class ProductService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repository = ProductRepository(db)

    async def create_product(self, product: Product) -> Product:
        return await self.repository.create(product)

    async def get_products(self) -> List[Product]:
        products = await self.repository.get_all()
        return [Product(**product) for product in products]

    async def get_product(self, product_id: str) -> Product:
        product = await self.repository.get_by_id(product_id)
        return Product(**product) 