from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import List, TYPE_CHECKING

from src.config.database import Base

if TYPE_CHECKING:
    from src.modules.quiz.entities import Category, Choice


class Question(Base):
    __tablename__ = "questions"

    uuid: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    category_uuid: Mapped[str] = mapped_column(String, ForeignKey("categories.uuid", ondelete="CASCADE"))

    category: Mapped["Category"] = relationship("Category", back_populates="questions")
    choices: Mapped[List["Choice"]] = relationship("Choice", back_populates="question", cascade="all, delete-orphan")