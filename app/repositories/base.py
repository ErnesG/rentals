from typing import Generic, TypeVar, List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.core.exceptions import NotFoundException, DatabaseException

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str):
        self.db = db
        self.collection = db[collection_name]
        self.entity_name = collection_name.rstrip('s').capitalize()

    async def create(self, entity: T) -> T:
        try:
            result = await self.collection.insert_one(entity.dict(by_alias=True))
            entity.id = str(result.inserted_id)
            return entity
        except Exception as e:
            raise DatabaseException("create", str(e))

    async def get_by_id(self, entity_id: str) -> Optional[T]:
        try:
            result = await self.collection.find_one({"_id": entity_id})
            if not result:
                raise NotFoundException(self.entity_name, entity_id)
            return result
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException("get_by_id", str(e))

    async def get_all(self) -> List[T]:
        try:
            return await self.collection.find().to_list(length=100)
        except Exception as e:
            raise DatabaseException("get_all", str(e)) 