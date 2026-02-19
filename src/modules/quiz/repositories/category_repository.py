from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import uuid7

from src.modules.quiz.entities import Category
from src.modules.quiz.models import CategoryResponseModel, CategoryCreateModel

class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def create(self, model: CategoryCreateModel) -> CategoryResponseModel:
        category = Category(
            uuid=str(uuid7()),
            **model.model_dump()
        )
        self._db.add(category)
        return category

    async def get_by_name(self, name: str) -> CategoryResponseModel:
        statement = select(Category).where(Category.name == name)
        result = await self._db.execute(statement)
        return result.scalar_one_or_none()