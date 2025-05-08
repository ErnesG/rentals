from app.models.user import User
from .base import BaseRepository
from app.core.exceptions import DatabaseException, NotFoundException

class UserRepository(BaseRepository[User]):
    def __init__(self, db):
        super().__init__(db, "users")
    
    async def get_by_email(self, email: str):
        try:
            result = await self.collection.find_one({"email": email})
            if not result:
                raise NotFoundException("User", f"with email {email}")
            return result
        except Exception as e:
            raise DatabaseException("get_by_email", str(e)) 