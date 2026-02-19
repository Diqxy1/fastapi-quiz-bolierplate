from decouple import config
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.models import LoginModel, LoginResponseModel
from src.modules.auth.repositories import TokenRepository

from src.modules.users.repositories import UserRepository
from src.modules.users.models import UserModel

from src.shared.middlewares.bcrypt import BcryptService
from src.shared.services.jwt_service import JwtService
from src.shared.exceptions import BadRequestException, NotFoundException

class LoginService:
    def __init__(self, db: AsyncSession):
        self._db = db
        self._secret_key = config("SECRET_KEY")
        self._issuer = config("JWT_ISSUER")
        self._audience = config("JWT_AUDIENCE")
        self._user_repository = UserRepository(db)
        self._token_repository = TokenRepository(db)
        self._bcrypt = BcryptService()
        self._jwt_service = JwtService()

    async def execute(self, model: LoginModel) -> LoginResponseModel:
        user = await self._validate_credentials(model)

        access_token = self._jwt_service._create_token(user, expires_minutes=15, scope="access_token")
        refresh_token = self._jwt_service._create_token(user, expires_minutes=60 * 24 * 7, scope="refresh_token")

        await self._token_repository.save(
            token=refresh_token, 
            user_uuid=user.uuid, 
            expires_days=7
        )

        await self._db.commit()

        return LoginResponseModel(
            access_token=access_token,
            token_type="Bearer",
            user=user,
            refresh_token=refresh_token
        )

    async def _validate_credentials(self, model: LoginModel) -> UserModel:
        user = await self._user_repository.get_by_username(model.username)

        if not user:
            raise NotFoundException("User not found")

        if not self._bcrypt.verify(model.password, user.password):
            raise BadRequestException("Invalid password")

        return user