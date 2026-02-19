from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


class CategoryCreateModel(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=255)

class CategoryResponseModel(BaseModel):
    uuid: str
    name: str
    description: Optional[str]
    model_config = ConfigDict(from_attributes=True)


class ChoiceCreateModel(BaseModel):
    text: str
    is_correct: bool


class ChoiceResponseModel(BaseModel):
    uuid: str
    text: str
    is_correct: bool
    model_config = ConfigDict(from_attributes=True)


class QuestionCreateModel(BaseModel):
    text: str
    category_uuid: str
    choices: List[ChoiceCreateModel] = Field(..., min_length=2, max_length=6)


class QuestionResponseModel(BaseModel):
    uuid: str
    text: str
    category_uuid: str
    choices: List[ChoiceResponseModel] 
    
    model_config = ConfigDict(from_attributes=True)


class ChoicePublicResponseModel(BaseModel):
    uuid: str
    text: str
    model_config = ConfigDict(from_attributes=True)


class QuestionPublicResponseModel(BaseModel):
    uuid: str
    text: str
    category_uuid: str
    choices: List[ChoicePublicResponseModel]
    model_config = ConfigDict(from_attributes=True)


class AnswerCheckModel(BaseModel):
    question_uuid: str
    choice_uuid: str


class AnswerResponseModel(BaseModel):
    correct: bool
    message: str
    correct_choice_uuid: Optional[str] = None


class RankingItemModel(BaseModel):
    username: str
    score: int


class RankingResponseModel(BaseModel):
    category_uuid: Optional[str] = None
    ranking: List[RankingItemModel]