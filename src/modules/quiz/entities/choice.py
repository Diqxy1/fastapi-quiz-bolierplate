from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Boolean
from typing import TYPE_CHECKING

from src.config.database import Base

if TYPE_CHECKING:
    from src.modules.quiz.entities import Question


class Choice(Base):
    __tablename__ = "choices"

    uuid: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    question_uuid: Mapped[str] = mapped_column(String, ForeignKey("questions.uuid", ondelete="CASCADE"))

    question: Mapped["Question"] = relationship("Question", back_populates="choices")