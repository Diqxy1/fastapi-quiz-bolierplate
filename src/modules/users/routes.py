from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_database

from src.modules.users.models import CreateUserModel, UserModel
from src.modules.users.services import (
    CreateUserService,
)

router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={404: {'description': 'Not Found'}}
)

@router.post('/create', response_model=UserModel)
async def create_user(
    model: CreateUserModel,
    db: AsyncSession = Depends(get_database)
):
    service = CreateUserService(db)
    return await service.execute(model)