from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.quiz.repositories import CategoryRepository
from src.modules.quiz.models import CategoryCreateModel, CategoryResponseModel

from src.shared.exceptions import BadRequestException

class CreateCategoryService:
    def __init__(self, db: AsyncSession):
        self._db = db
        self._repo = CategoryRepository(db)

    async def execute(self, model: CategoryCreateModel) -> CategoryResponseModel:
        existing = await self._repo.get_by_name(model.name)

        if existing:
            raise BadRequestException("Category already exists")

        category = await self._repo.create(model)

        try:
            await self._db.commit()
            return category
        except Exception as e:
            await self._db.rollback()
            raise e