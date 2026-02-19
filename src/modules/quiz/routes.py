from typing import Union, List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_database

from src.modules.users.models import UserModel

from src.modules.quiz.models import (
    CategoryCreateModel, 
    CategoryResponseModel, 
    QuestionCreateModel, 
    QuestionResponseModel,
    QuestionPublicResponseModel,
    AnswerCheckModel,
    AnswerResponseModel,
    RankingResponseModel
)
from src.modules.quiz.services import (
    CreateCategoryService,
    CreateQuestionService,
    ListQuestionsService,
    AnswerQuestionService,
    GetRankingService
)

from src.shared.middlewares.dependencies import get_current_staff_user, get_current_user

router = APIRouter(
    prefix='/quiz',
    tags=['quiz'],
    responses={404: {'description': 'Not Found'}}
)

@router.post('/create/category', response_model=CategoryResponseModel)
async def create_category(
    model: CategoryCreateModel,
    db: AsyncSession = Depends(get_database),
    _: UserModel = Depends(get_current_staff_user)
):
    service = CreateCategoryService(db)
    return await service.execute(model)

@router.post('/create/question', response_model=QuestionResponseModel)
async def create_question(
    model: QuestionCreateModel,
    db: AsyncSession = Depends(get_database),
    _: UserModel = Depends(get_current_staff_user)
):
    service = CreateQuestionService(db)
    return await service.execute(model)

@router.get('/categories', response_model=Union[List[QuestionResponseModel], List[QuestionPublicResponseModel]])
async def list_questions(
    category: str = None,
    db: AsyncSession = Depends(get_database),
    current_user: UserModel = Depends(get_current_user)
):
    service = ListQuestionsService(db)
    questions = await service.execute(category)

    if current_user.is_staff:
        return [QuestionResponseModel.model_validate(q) for q in questions]

    return [QuestionPublicResponseModel.model_validate(q) for q in questions]

@router.post('/answer', response_model=AnswerResponseModel)
async def answer_question(
    model: AnswerCheckModel,
    db: AsyncSession = Depends(get_database),
    current_user: UserModel = Depends(get_current_user)
):
    service = AnswerQuestionService(db)
    return await service.execute(model, current_user)

@router.get('/ranking', response_model=RankingResponseModel)
async def get_ranking(
    category_uuid: Optional[str] = None,
    db: AsyncSession = Depends(get_database),
    _: UserModel = Depends(get_current_user)
):
    service = GetRankingService(db)
    return await service.execute(category_uuid)