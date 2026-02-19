from uuid6 import uuid7
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.quiz.entities import Question, Choice, Category

from src.modules.users.entities import UserCategoryScore


class QuestionRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def create_with_choices(self, text: str, category_uuid: str, choices_data: list) -> Question:
        question = Question(
            uuid=str(uuid7()),
            text=text,
            category_uuid=category_uuid
        )

        self._db.add(question)

        for c in choices_data:
            choice = Choice(
                uuid=str(uuid7()),
                text=c.text,
                is_correct=c.is_correct,
                question_uuid=question.uuid
            )
            self._db.add(choice)
        
        await self._db.flush()
        
        statement = (
            select(Question)
            .options(selectinload(Question.choices))
            .where(Question.uuid == question.uuid)
        )

        result = await self._db.execute(statement)
        
        return result.scalar_one()

    async def get_by_category_name(self, category_name: str) -> list[Question]:
        statement = (
            select(Question)
            .join(Category)
            .options(selectinload(Question.choices))
            .where(Category.name.ilike(f"%{category_name}%"))
        )
        
        result = await self._db.execute(statement)
        return list(result.scalars().all())
    
    async def validate_answer(self, question_uuid: str, choice_uuid: str) -> Choice:
        statement = (
            select(Choice)
            .options(joinedload(Choice.question))
            .where(Choice.uuid == choice_uuid)
            .where(Choice.question_uuid == question_uuid)
        )
        result = await self._db.execute(statement)
        return result.scalar_one_or_none()

    async def get_correct_choice(self, question_uuid: str) -> Choice:
        statement = (
            select(Choice)
            .where(Choice.question_uuid == question_uuid)
            .where(Choice.is_correct == True)
        )
        result = await self._db.execute(statement)
        return result.scalar_one_or_none()

    async def update_category_score(self, user_uuid: str, category_uuid: str, points: int):
        statement = select(UserCategoryScore).where(
            UserCategoryScore.user_uuid == user_uuid,
            UserCategoryScore.category_uuid == category_uuid
        )
        result = await self._db.execute(statement)
        user_cat_score = result.scalar_one_or_none()

        if user_cat_score:
            user_cat_score.score += points
        else:
            new_score = UserCategoryScore(
                uuid=str(uuid7()),
                user_uuid=user_uuid,
                category_uuid=category_uuid,
                score=points
            )
            self._db.add(new_score)
        
        await self._db.flush()