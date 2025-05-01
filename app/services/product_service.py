from app.core.database import db
from app.models.product import Product
from typing import List

class ProductService:
    @staticmethod
    async def create_product(product: Product) -> Product:
        result = await db.products.insert_one(product.dict(by_alias=True))
        product.id = str(result.inserted_id)
        return product

    @staticmethod
    async def get_products() -> List[Product]:
        products = await db.products.find().to_list(length=100)
        return [Product(**product) for product in products] 