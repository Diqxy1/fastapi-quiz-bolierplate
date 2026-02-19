from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_database

from src.modules.auth.models import LoginModel, LoginResponseModel, RefreshRequestModel, RefreshTokenResponseModel
from src.modules.auth.services import (
    LoginService,
    RefreshTokenService
)

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={404: {'description': 'Not Found'}}
)

@router.post('/login', response_model=LoginResponseModel)
async def login(
    model: LoginModel,
    db: AsyncSession = Depends(get_database)
):
    service = LoginService(db)
    return await service.execute(model)

@router.patch('/refresh', response_model=RefreshTokenResponseModel)
async def refresh(
    model: RefreshRequestModel,
    db: AsyncSession = Depends(get_database)
):
    service = RefreshTokenService(db)
    return await service.execute(model)