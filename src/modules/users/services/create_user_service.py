from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.models import CreateUserModel, UserModel
from src.modules.users.repositories import UserRepository

from src.shared.middlewares.bcrypt import BcryptService
from src.shared.exceptions import BadRequestException

class CreateUserService:

    def __init__(self, db: AsyncSession):
        self._db = db
        self._repository = UserRepository(db)
        self._bcrypt = BcryptService()

    async def execute(self, create_user_model: CreateUserModel) -> UserModel:
        # validations
        await self._make_validations(create_user_model)
        # create user
        user = await self._create(create_user_model)
        return user

    async def _create(self, create_user_model: CreateUserModel) -> UserModel:
        create_user_model.password = self._bcrypt.hash(create_user_model.password)

        user = await self._repository.create_user(create_user_model)

        await self._db.commit()
        await self._db.refresh(user)

        return user

    async def _make_validations(self, create_user_model: CreateUserModel):
        user_exist = await self._repository.get_by_username(create_user_model.username)

        if user_exist:
            raise BadRequestException(message='Username already in use')
        
        if not create_user_model.username or not create_user_model.password:
            raise BadRequestException("Username and password are required")

        if len(create_user_model.password) < 6:
            raise BadRequestException("Password must be at least 6 characters long")