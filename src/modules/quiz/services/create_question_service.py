from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.quiz.repositories import QuestionRepository
from src.modules.quiz.models import QuestionCreateModel

from src.shared.exceptions import BadRequestException

class CreateQuestionService:
    def __init__(self, db: AsyncSession):
        self._db = db
        self._repo = QuestionRepository(db)

    async def execute(self, model: QuestionCreateModel):

        correct_choices = [c for c in model.choices if c.is_correct]
        if len(correct_choices) != 1:
            raise BadRequestException("A question must have exactly one correct answer.")

        try:
            question = await self._repo.create_with_choices(
                text=model.text,
                category_uuid=model.category_uuid,
                choices_data=model.choices
            )

            await self._db.commit()
            return question

        except Exception as e:
            await self._db.rollback()
            raise e