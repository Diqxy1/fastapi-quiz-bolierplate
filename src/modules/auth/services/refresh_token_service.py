from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.models import RefreshTokenResponseModel, RefreshRequestModel
from src.modules.auth.repositories import TokenRepository

from src.modules.users.repositories import UserRepository
from src.modules.users.models import UserModel

from src.shared.services.jwt_service import JwtService
from src.shared.exceptions import UnauthorizedException

class RefreshTokenService:
    def __init__(self, db: AsyncSession):
        self._db = db
        self._token_repo = TokenRepository(db)
        self._user_repo = UserRepository(db)
        self._jwt_service = JwtService()

    async def execute(self, model: RefreshRequestModel) -> RefreshTokenResponseModel:
        payload = self._jwt_service.decode_token(model.refresh_token)

        user = await self.make_validations(payload, model)

        try:
            await self._token_repo.revoke(model.refresh_token)

            new_access_token = self._jwt_service._create_token(user, expires_minutes=15, scope="access_token")
            new_refresh_token = self._jwt_service._create_token(user, expires_minutes=60 * 24 * 7, scope="refresh_token")

            await self._token_repo.save(
                token=new_refresh_token,
                user_uuid=user.uuid,
                expires_days=7
            )

            await self._db.commit()

            return RefreshTokenResponseModel(
                access_token=new_access_token,
                refresh_token=new_refresh_token,
                token_type="Bearer",
                user=user
            )
        except Exception as e:
            await self._db.rollback()
            raise e

    async def make_validations(self, payload: dict, model: RefreshRequestModel) -> UserModel:
        if payload.get("scope") != "refresh_token":
            raise UnauthorizedException("Invalid token scope")

        is_valid = await self._token_repo.is_valid(model.refresh_token)
        if not is_valid:
            raise UnauthorizedException("Token revoked or not found in database")

        user = await self._user_repo.get_by_uuid(payload.get("sub"))
        if not user:
            raise UnauthorizedException("User associated with token not found")
        
        return user