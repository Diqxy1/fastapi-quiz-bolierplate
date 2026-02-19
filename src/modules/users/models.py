from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    username: str

class CreateUserModel(UserBase):
    password: str

class UserModel(UserBase):
    uuid: str
    password: str
    is_staff: bool
    total_score: int
    
    model_config = ConfigDict(from_attributes=True)