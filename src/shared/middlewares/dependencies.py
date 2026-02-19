from fastapi import Depends
from decouple import config
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBearer

from src.config.database import get_database
from src.modules.users.repositories import UserRepository
from src.modules.users.models import UserModel

from src.shared.exceptions import UnauthorizedException, BadRequestException, ForbiddenException

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = "HS256"
ISSUER = config("JWT_ISSUER", default="myapp")
AUDIENCE = config("JWT_AUDIENCE", default="myapp_users")

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPBearer = Depends(security),
    db: AsyncSession = Depends(get_database),
) -> UserModel:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            audience=AUDIENCE,
            issuer=ISSUER,
            options={"require": ["exp", "iss", "aud", "sub"]}
        )
        user_uuid: str = payload.get("sub")

        if user_uuid is None:
            raise UnauthorizedException("Invalid credentials")

        repository = UserRepository(db)
        user = await repository.get_by_uuid(user_uuid)

        if user is None:
            raise BadRequestException("Account not found")

        return user

    except JWTError:
        raise UnauthorizedException("Invalid credentials")
    except Exception as e:
        print("JWT Exception", e)
        raise UnauthorizedException("Could not validate credentials")
    
async def get_current_staff_user(
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.is_staff:
        raise ForbiddenException("You do not have permission to perform this action")
    
    return current_user