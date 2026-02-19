from pydantic import BaseModel, ConfigDict, Field
from src.modules.users.models import UserModel


class TokenBaseModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    user: UserModel

    model_config = ConfigDict(from_attributes=True)


class LoginModel(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

    model_config = ConfigDict(from_attributes=True)


class LoginResponseModel(TokenBaseModel):
    pass


class RefreshTokenResponseModel(TokenBaseModel):
    pass


class RefreshRequestModel(BaseModel):
    refresh_token: str