from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.modules.quiz.repositories import QuestionRepository
from src.modules.quiz.models import QuestionResponseModel

from src.shared.exceptions import BadRequestException

class ListQuestionsService:
    def __init__(self, db: AsyncSession):
        self._db = db
        self._repo = QuestionRepository(db)

    async def execute(self, category: str = None) -> List[QuestionResponseModel]:
        questions = await self._repo.get_by_category_name(category)

        if not questions:
            raise BadRequestException("No questions found for this category")

        return questions