from uuid6 import uuid7
from typing import List, Optional
from sqlalchemy import delete, select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.entities import User, UserCategoryScore
from src.modules.users.models import CreateUserModel, UserModel

class UserRepository:

    def __init__(self, db: AsyncSession):
        self._db = db

    async def create_user(self, model: CreateUserModel) -> User:
        user = User(**model.model_dump())
        user.uuid = str(uuid7())

        self._db.add(user)
        await self._db.flush() 
        return user

    async def get_by_uuid(self, uuid: str) -> Optional[User]:
        statement = select(User).where(User.uuid == uuid)
        result = await self._db.execute(statement)
        return result.scalars().first()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        statement = select(User).where(User.username == username)
        result = await self._db.execute(statement)
        return result.scalars().first()


    async def update_user(self, uuid: str, model: CreateUserModel) -> UserModel | None:
        statement = select(User).where(User.uuid == uuid)
        result = await self._db.execute(statement)
        user = result.scalars().first()

        if not user:
            return None

        user.username = model.username
        user.password = model.password

        await self._db.commit()
        await self._db.refresh(user)

        return UserModel.model_validate(user)

    async def delete_user(self, uuid: str) -> bool:
        try:
            statement = delete(User).where(User.uuid == uuid)
            await self._db.execute(statement)
            await self._db.commit()
            return True
        except Exception:
            return False

    async def get_top_ranking(self, limit: int = 10) -> list[User]:
        statement = (
            select(User)
            .order_by(User.total_score.desc())
            .limit(limit)
        )
        result = await self._db.execute(statement)
        return list(result.scalars().all())
    
    async def get_category_ranking(self, category_uuid: str, limit: int = 10) -> List[User]:
        statement = (
            select(
                User.username,
                UserCategoryScore.score
            )
            .join(User, User.uuid == UserCategoryScore.user_uuid)
            .where(UserCategoryScore.category_uuid == category_uuid)
            .order_by(UserCategoryScore.score.desc())
            .limit(limit)
        )
        
        result = await self._db.execute(statement)
        return result.all()

    async def get_general_ranking(self, limit: int = 10) -> List[User]:
        statement = (
            select(User)
            .order_by(User.total_score.desc())
            .limit(limit)
        )
        result = await self._db.execute(statement)
        return list(result.scalars().all())
    
    async def refresh_total_score(self, user_uuid: str):
        statement = select(func.sum(UserCategoryScore.score)).where(UserCategoryScore.user_uuid == user_uuid)
        result = await self._db.execute(statement)
        total = result.scalar() or 0

        final_score = max(0, total)
        
        update_statement = update(User).where(User.uuid == user_uuid).values(total_score=final_score)
        await self._db.execute(update_statement)