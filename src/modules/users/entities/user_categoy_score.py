from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer

from src.config.database import Base


class UserCategoryScore(Base):
    __tablename__ = 'user_category_scores'

    uuid: Mapped[str] = mapped_column(String, primary_key=True)
    user_uuid: Mapped[str] = mapped_column(String, index=True)
    category_uuid: Mapped[str] = mapped_column(String, index=True)
    score: Mapped[int] = mapped_column(Integer, default=0)