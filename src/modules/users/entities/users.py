from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, func, Boolean
from datetime import datetime
from typing import List, TYPE_CHECKING

from src.config.database import Base

if TYPE_CHECKING:
    from src.modules.auth.entities import RefreshToken

class User(Base):

    __tablename__ = 'users'

    uuid: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    total_score: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        server_default=func.now(), 
        onupdate=func.now() 
    )

    # relations
    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(
        "RefreshToken", 
        back_populates="user", 
        cascade="all, delete-orphan"
    )