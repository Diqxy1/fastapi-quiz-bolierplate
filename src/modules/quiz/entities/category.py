from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import List, TYPE_CHECKING

from src.config.database import Base

if TYPE_CHECKING:
    from src.modules.quiz.entities import Question


class Category(Base):
    __tablename__ = "categories"

    uuid: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    questions: Mapped[List["Question"]] = relationship("Question", back_populates="category")