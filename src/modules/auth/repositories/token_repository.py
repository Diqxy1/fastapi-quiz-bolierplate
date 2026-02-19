from uuid6 import uuid7
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone, timedelta

from src.modules.auth.entities.refresh_token import RefreshToken

class TokenRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def save(self, token: str, user_uuid: str, expires_days: int = 7):
        now_naive = datetime.now(timezone.utc).replace(tzinfo=None)

        statement = delete(RefreshToken).where(
            RefreshToken.user_uuid == user_uuid,
            RefreshToken.expires_at < now_naive
        )
        await self._db.execute(statement)

        db_token = RefreshToken(
            uuid=str(uuid7()),
            token=token,
            user_uuid=user_uuid,
            expires_at=now_naive + timedelta(days=expires_days),
            revoked=False
        )
        self._db.add(db_token)
        return db_token
    
    async def is_valid(self, token: str) -> bool:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        
        statement = select(RefreshToken).where(
            RefreshToken.token == token,
            RefreshToken.revoked == False,
            RefreshToken.expires_at > now 
        )
        
        result = await self._db.execute(statement)
        db_token = result.scalar_one_or_none()

        return db_token is not None

    async def revoke(self, token: str):
        statement = (
            update(RefreshToken)
            .where(RefreshToken.token == token)
            .values(revoked=True)
        )
        await self._db.execute(statement)