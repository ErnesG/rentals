from app.models.product import Product
from .base import BaseRepository

class ProductRepository(BaseRepository[Product]):
    def __init__(self, db):
        super().__init__(db, "products") 