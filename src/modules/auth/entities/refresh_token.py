from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base

from src.modules.users.entities import User


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    uuid: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    token: Mapped[str] = mapped_column(String, nullable=False)
    user_uuid: Mapped[str] = mapped_column(
        String, ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped[User] = relationship("User", back_populates="refresh_tokens")