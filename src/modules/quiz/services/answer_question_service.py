from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.modules.quiz.repositories import QuestionRepository
from src.modules.quiz.models import AnswerCheckModel, AnswerResponseModel

from src.modules.users.models import UserModel
from src.modules.users.repositories import UserRepository

from src.shared.exceptions import BadRequestException

class AnswerQuestionService:
    def __init__(self, db: AsyncSession):
        self._db = db
        self._repo = QuestionRepository(db)
        self._user_repo = UserRepository(db)
        self._points = 0

    async def execute(self, model: AnswerCheckModel, user: UserModel) -> AnswerResponseModel:
        choice = await self._repo.validate_answer(
            question_uuid=model.question_uuid,
            choice_uuid=model.choice_uuid
        )

        if not choice:
            raise BadRequestException("Essa alternativa não pertence a esta pergunta ou não existe.")

        points_to_apply = 1 if choice.is_correct else -1

        await self._repo.update_category_score(
            user_uuid=user.uuid,
            category_uuid=choice.question.category_uuid,
            points=points_to_apply
        )

        await self._user_repo.refresh_total_score(user.uuid)

        await self._db.commit()

        if choice.is_correct:
            return AnswerResponseModel(
                correct=True,
                message="Mandou bem! +1 ponto."
            )

        correct_one = await self._repo.get_correct_choice(model.question_uuid)
        
        return AnswerResponseModel(
            correct=False,
            message="Putz, não foi dessa vez. -1 ponto",
            correct_choice_uuid=correct_one.uuid if correct_one else None
        )