from typing import Optional
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.auth import get_password_hash, verify_password
from motor.motor_asyncio import AsyncIOMotorDatabase

class UserService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repository = UserRepository(db)

    async def create_user(self, user: User) -> User:
        # Hash password before storing
        user.password = get_password_hash(user.password)
        return await self.repository.create(user)

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = await self.repository.get_by_email(email)
        if not user or not verify_password(password, user.password):
            return None
        return User(**user) 